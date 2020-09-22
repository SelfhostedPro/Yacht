from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..db import models, schemas
from ..utils import *

from datetime import datetime
import docker


def get_running_apps():
    apps_list = []
    dclient = docker.from_env()
    apps = dclient.containers.list()
    for app in apps:
        attrs = app.attrs
        attrs.update(conv2dict('name', app.name))
        attrs.update(conv2dict('ports', app.ports))
        attrs.update(conv2dict('short_id', app.short_id))
        apps_list.append(attrs)

    return apps_list

def get_apps():
    apps_list = []
    dclient = docker.from_env()
    apps = dclient.containers.list(all=True)
    for app in apps:
        attrs = app.attrs
        attrs.update(conv2dict('name', app.name))
        attrs.update(conv2dict('ports', app.ports))
        attrs.update(conv2dict('short_id', app.short_id))
        apps_list.append(attrs)

    return apps_list


def get_app(app_name):
    dclient = docker.from_env()
    app = dclient.containers.get(app_name)
    attrs = app.attrs

    attrs.update(conv2dict('ports', app.ports))
    attrs.update(conv2dict('short_id', app.short_id))
    attrs.update(conv2dict('name', app.name))

    return attrs


def get_app_processes(app_name):
    dclient = docker.from_env()
    app = dclient.containers.get(app_name)
    if app.status == 'running':
        processes = app.top()
        return schemas.Processes(Processes=processes['Processes'], Titles=processes['Titles'])
    else:
        return None


def get_app_logs(app_name):
    dclient = docker.from_env()
    app = dclient.containers.get(app_name)
    if app.status == 'running':
        return schemas.AppLogs(logs=app.logs())
    else:
        return None


def deploy_app(template: schemas.DeployForm):
    try:
        launch = launch_app(
            template.name,
            template.image,
            conv_restart2data(template.restart_policy),
            conv_ports2data(template.ports),
            conv_volumes2data(template.volumes),
            conv_env2data(template.env),
            conv_sysctls2data(template.sysctls),
            conv_caps2data(template.cap_add)
        )

    except Exception as exc:
        raise
    print('done deploying')

    return schemas.DeployLogs(logs=launch.logs())


def launch_app(name, image, restart_policy, ports, volumes, env, sysctls, caps):
    dclient = docker.from_env()
    lauch = dclient.containers.run(
        name=name,
        image=image,
        restart_policy=restart_policy,
        ports=ports,
        volumes=volumes,
        environment=env,
        sysctls=sysctls,
        cap_add=caps,
        detach=True
    )
    print(lauch)
    print(f'''Container started successfully.
       Name: {name},
      Image: {image},
      Ports: {ports},
    Volumes: {volumes},
        Env: {env}''')
    return lauch


def app_action(app_name, action):
    err = None
    dclient = docker.from_env()
    app = dclient.containers.get(app_name)
    _action = getattr(app, action)
    if action == 'remove':
        try:
            _action(force=True)
        except Exception as exc:
            err = f"{exc}"
    else:
        try:
            _action()
        except Exception as exc:
            err = exc.explination
    apps_list = get_apps()
    return apps_list

def prune_images():
    dclient = docker.from_env()
    deleted_everything = {}
    deleted_volumes = dclient.volumes.prune()
    deleted_images = dclient.images.prune()
    deleted_networks = dclient.networks.prune()

    deleted_everything.update(deleted_networks)
    deleted_everything.update(deleted_volumes)
    deleted_everything.update(deleted_images)
    
    return deleted_everything