from .db import models
from .db.database import SessionLocal
import re
from typing import Dict, List, Optional

from jose import jwt
from fastapi import Cookie, Depends, WebSocket, status
from fastapi.security import APIKeyCookie
from .auth import cookie_authentication
from .auth import user_db
from .settings import Settings
settings = Settings()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#For Templates
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
def conv_ports2dict(data: List[str]) -> List[Dict[str,str]]:
    delim = ':'
    portlst = []
    for port_data in data:
        if not re.match(REGEXP_PORT_ASSIGN, port_data, flags=re.IGNORECASE):
            raise ValueError('Malformed port assignment.')

        hport,cport = None,port_data
        if delim in cport:
            hport,cport = cport.split(delim, 1)
            if not hport: hport = None
        cport,proto = cport.split('/', 1)
        portlst.append({ 'cport': cport, 'hport': hport, 'proto': proto })
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
    return [{ 'name': k, 'value': v } for item in data for k,v in item.items()]

def conv2dict(name, value):
    _tmp_attr = { name: value}
    return _tmp_attr


### For Deploy Form

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
        if not hport: hport = None
        ports.update({str(cport)+'/'+proto:hport for d in data})
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
                  new_path = volume.bind.replace(t_var.variable, t_var.replacement)
                  volume.bind = new_path
    volume_data = dict((d.bind, {'bind': d.container, 'mode': 'rw'}) for d in data)

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