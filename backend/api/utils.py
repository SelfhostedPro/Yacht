from .db import models
from .db.database import SessionLocal
import re
from typing import Dict, List, Optional

from jose import jwt
from fastapi import Cookie, Depends, WebSocket, status, HTTPException
from fastapi.security import APIKeyCookie
from .auth import cookie_authentication
from .auth import user_db
from .settings import Settings
import aiodocker
import json
settings = Settings()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# For Templates
REGEXP_PORT_ASSIGN = r'^(?:(?:\d{1,5}:)?\d{1,5}|:\d{1,5})/(?:tcp|udp)$'

# Input Format:
# [
#     '80:8080/tcp',
#     '123:123/udp'
#     '4040/tcp',
# ]
# Result Format:
# [
#     {
#         'cport': '80',
#         'hport': '8080',
#         'proto': 'tcp',
#     },
#     ...
# ]


def conv_ports2dict(data: List[str]) -> List[Dict[str, str]]:
    if type(data[0]) == dict:
        delim = ':'
        portlst = []
        for port_data in data:
            for label, port in port_data.items():
                if not re.match(REGEXP_PORT_ASSIGN, port, flags=re.IGNORECASE):
                    raise ValueError('Malformed port assignment.')

                hport, cport = None, port
                if delim in cport:
                    hport, cport = cport.split(delim, 1)
                    if not hport:
                        hport = None
                cport, proto = cport.split('/', 1)
                portlst.append({'cport': cport, 'hport': hport, 'proto': proto, 'label': label})
            return portlst

    elif type(data) == list:
        delim = ':'
        portlst = []
        for port_data in data:
            if not re.match(REGEXP_PORT_ASSIGN, port_data, flags=re.IGNORECASE):
                raise ValueError('Malformed port assignment.')

            hport, cport = None, port_data
            if delim in cport:
                hport, cport = cport.split(delim, 1)
                if not hport:
                    hport = None
            cport, proto = cport.split('/', 1)
            portlst.append({'cport': cport, 'hport': hport, 'proto': proto})
        return portlst

# Input Format:
# [
#     {
#         'net.ipv6.conf.all.disable_ipv6': '0'
#     }
# ]
# Result Format:
# [
#     {
#         'name': 'net.ipv6.conf.all.disable_ipv6',
#         'value': '0'
#     }
# ]


def conv_sysctls2dict(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return [{'name': k, 'value': v} for item in data for k, v in item.items()]


def conv2dict(name, value):
    _tmp_attr = {name: value}
    return _tmp_attr


# For Deploy Form

# Input Format:
# [
#     {
#         'cport': '53',
#         'hport': '53',
#         'proto': 'tcp',
#     },
#     ...
# ]
# Result Format:
# {
#     '53/tcp': ('0.0.0.0', 53),
# }
def conv_ports2data(data):
    ports = {}
    for d in data:
        cport = d.cport
        hport = d.hport
        proto = d.proto
        if not hport:
            hport = None
        ports.update({str(cport)+'/'+proto: hport for d in data})
    return ports

# Input Format:
# [
#     {
#         'container': '/mnt/vol2',
#         'bind': '/home/user1'
#     }
#     ...
# ]
# Result Format:
# {
#     '/home/user1/': {'bind': '/mnt/vol2', 'mode': 'rw'},
#     '/var/www': {'bind': '/mnt/vol1', 'mode': 'ro'}
# }


def conv_volumes2data(data):
    db = SessionLocal()
    t_variables = db.query(models.TemplateVariables).all()

    for volume in data:
        if volume.bind:
            for t_var in t_variables:
                if t_var.variable in volume.bind:
                    new_path = volume.bind.replace(
                        t_var.variable, t_var.replacement)
                    volume.bind = new_path
    volume_data = dict(
        (d.bind, {'bind': d.container, 'mode': 'rw'}) for d in data)

    return volume_data


# Input Format:
# [
#     {
#         'name': 'SOMEVARIABLE',
#         'default': '1000'
#     }
#     ...
# ]
# Result Format:
# [
#     "SOMEVARIABLE=xxx", "OTHERVARIABLE=yyy"
# ]
def conv_env2data(data):
    # Set is depracated. Name is the actual value. Label is the name of the field.
    # Label is the label of the label field.
    delim = '='
    return [delim.join((d.name, d.default)) for d in data]


def conv_sysctls2data(data):
    if data:
        return dict((d.name, d.value) for d in data)
    else:
        sysctls = None
        return sysctls


def conv_caps2data(data):
    if data:
        return data
    else:
        caps = None
        return caps


def conv_restart2data(data):
    if data:
        return {'name': data}
    else:
        restart = None
        return restart


async def websocket_auth(
    websocket: WebSocket
):
    try:
        cookie = websocket._cookies['fastapiusersauth']
        user = await cookie_authentication(cookie, user_db)
        if user and user.is_active:
            return user
    except:
        return None

async def calculate_cpu_percent(d):
    cpu_count = len(d["cpu_stats"]["cpu_usage"]["percpu_usage"])
    cpu_percent = 0.0
    cpu_delta = float(d["cpu_stats"]["cpu_usage"]["total_usage"]) - \
        float(d["precpu_stats"]["cpu_usage"]["total_usage"])
    system_delta = float(d["cpu_stats"]["system_cpu_usage"]) - \
        float(d["precpu_stats"]["system_cpu_usage"])
    if system_delta > 0.0:
        cpu_percent = cpu_delta / system_delta * 100.0 * cpu_count
    return cpu_percent


async def calculate_cpu_percent2(d, previous_cpu, previous_system):
    cpu_percent = 0.0
    cpu_total = float(d["cpu_stats"]["cpu_usage"]["total_usage"])
    cpu_delta = cpu_total - previous_cpu
    cpu_system = float(d["cpu_stats"]["system_cpu_usage"])
    system_delta = cpu_system - previous_system
    online_cpus = d["cpu_stats"].get("online_cpus", len(
        d["cpu_stats"]["cpu_usage"]["percpu_usage"]))
    if system_delta > 0.0:
        cpu_percent = (cpu_delta / system_delta) * online_cpus * 100.0
    return cpu_percent, cpu_system, cpu_total


async def calculate_blkio_bytes(d):
    bytes_stats = graceful_chain_get(
        d, "blkio_stats", "io_service_bytes_recursive")
    if not bytes_stats:
        return 0, 0
    r = 0
    w = 0
    for s in bytes_stats:
        if s["op"] == "Read":
            r += s["value"]
        elif s["op"] == "Write":
            w += s["value"]
    return r, w


async def calculate_network_bytes(d):
    networks = graceful_chain_get(d, "networks")
    if not networks:
        return 0, 0
    r = 0
    t = 0
    for if_name, data in networks.items():
        r += data["rx_bytes"]
        t += data["tx_bytes"]
    return r, t


def graceful_chain_get(d, *args, default=None):
    t = d
    for a in args:
        try:
            t = t[a]
        except (KeyError, ValueError, TypeError, AttributeError):
            print("can't get %r from %s", a, t)
            return default
    return t


async def get_app_stats(app_name):
    async with aiodocker.Docker() as docker:
        cpu_total = 0.0
        cpu_system = 0.0
        cpu_percent = 0.0

        container: DockerContainer = await docker.containers.get(app_name)
        stats = container.stats(stream=True)
        async for line in stats:
            mem_current = line["memory_stats"]["usage"]
            mem_total = line["memory_stats"]["limit"]

            try:
                cpu_percent, cpu_system, cpu_total = await calculate_cpu_percent2(line, cpu_total, cpu_system)
            except KeyError as e:
                print("error while getting new CPU stats: %r, falling back")
                cpu_percent = await calculate_cpu_percent(line)

            full_stats = {
                "name": line['name'],
                "time": line['read'],
                "cpu_percent": cpu_percent,
                "mem_current": mem_current,
                "mem_total": line["memory_stats"]["limit"],
                "mem_percent": (mem_current / mem_total) * 100.0,
            }
            yield json.dumps(full_stats)
