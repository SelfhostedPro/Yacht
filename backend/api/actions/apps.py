from fastapi import HTTPException

from api.db.schemas.apps import (
    DeployLogs,
    DeployForm,
    AppLogs,
    Processes
)
from api.utils.apps import (
    conv_caps2data,
    conv_devices2data,
    conv_env2data,
    conv_image2data,
    conv_labels2data,
    conv_portlabels2data,
    conv_ports2data,
    conv_restart2data,
    conv_sysctls2data,
    conv_volumes2data,
    _check_updates,
)
from api.utils.templates import conv2dict

import time
import subprocess
import docker

"""
Returns all running apps in a list
"""


def get_running_apps():
    apps_list = []
    dclient = docker.from_env()
    apps = dclient.containers.list()
    for app in apps:
        attrs = app.attrs
        attrs.update(conv2dict("name", app.name))
        attrs.update(conv2dict("ports", app.ports))
        attrs.update(conv2dict("short_id", app.short_id))
        apps_list.append(attrs)

    return apps_list


"""
Checks repo digest for app and compares it to image
digest to see if there's an update available.

TODO: This has issues if there's more than one repo digest
"""


def check_app_update(app_name):
    dclient = docker.from_env()
    try:
        app = dclient.containers.get(app_name)
    except Exception as exc:
        raise HTTPException(
            status_code=exc.response.status_code, detail=exc.explanation
        )

    if app.attrs["Config"]["Image"]:
        if _check_updates(app.attrs["Config"]["Image"]):
            app.attrs.update(conv2dict("isUpdatable", True))
    app.attrs.update(conv2dict("name", app.name))
    app.attrs.update(conv2dict("ports", app.ports))
    app.attrs.update(conv2dict("short_id", app.short_id))
    return app.attrs


"""
Gets all apps in a list and add some easy access to
properties that aren't in the app attributes
"""


def get_apps():
    apps_list = []
    try:
        dclient = docker.from_env()
    except docker.errors.DockerException as exc:
        raise HTTPException(status_code=500, detail=exc.args)
    try:
        apps = dclient.containers.list(all=True)
    except Exception as exc:
        raise HTTPException(
            status_code=exc.response.status_code, detail=exc.explanation
        )
    for app in apps:
        attrs = app.attrs

        attrs.update(conv2dict("name", app.name))
        attrs.update(conv2dict("ports", app.ports))
        attrs.update(conv2dict("short_id", app.short_id))
        apps_list.append(attrs)

    return apps_list


"""
Get a single app by the container name and some easy 
access to properties that aren't in the app 
attributes
"""


def get_app(app_name):
    dclient = docker.from_env()
    try:
        app = dclient.containers.get(app_name)
    except Exception as exc:
        raise HTTPException(
            status_code=exc.response.status_code, detail=exc.explanation
        )
    attrs = app.attrs

    attrs.update(conv2dict("ports", app.ports))
    attrs.update(conv2dict("short_id", app.short_id))
    attrs.update(conv2dict("name", app.name))

    return attrs


"""
Get processes running in an app.
"""


def get_app_processes(app_name):
    dclient = docker.from_env()
    app = dclient.containers.get(app_name)
    if app.status == "running":
        processes = app.top()
        return Processes(
            Processes=processes["Processes"], Titles=processes["Titles"]
        )
    else:
        return None


"""
Get app logs (this isn't in use as logs are served
via a websocket in routers so they're realtime)
"""


def get_app_logs(app_name):
    dclient = docker.from_env()
    app = dclient.containers.get(app_name)
    if app.status == "running":
        return AppLogs(logs=app.logs())
    else:
        return None


"""
Deploy a new app. Format is available in 
../db/schemas/apps.py
"""


def deploy_app(template: DeployForm):
    try:
        launch = launch_app(
            template.name,
            conv_image2data(template.image),
            conv_restart2data(template.restart_policy),
            conv_ports2data(template.ports, template.network, template.network_mode),
            conv_portlabels2data(template.ports),
            template.network_mode,
            template.network,
            conv_volumes2data(template.volumes),
            conv_env2data(template.env),
            conv_devices2data(template.devices),
            conv_labels2data(template.labels),
            conv_sysctls2data(template.sysctls),
            conv_caps2data(template.cap_add),
            edit=template.edit or False,
            id=template.id or None
        )
    except HTTPException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)
    except Exception as exc:
        raise HTTPException(
            status_code=exc.response.status_code, detail=exc.explanation
        )
    print("done deploying")

    return DeployLogs(logs=launch.logs())


"""
Merge utility used for combining portlabels and
labels into a single variable
"""


def Merge(dict1, dict2):
    if dict1 and dict2:
        dict2.update(dict1)
        return dict2
    elif dict1:
        return dict1
    elif dict2:
        return dict2
    else:
        return None


"""
This function actually runs the docker run command.
It also checks if edit is set to true so it can 
remove the container you're editing before deploying
a new one.
"""


def launch_app(
    name,
    image,
    restart_policy,
    ports,
    portlabels,
    network_mode,
    network,
    volumes,
    env,
    devices,
    labels,
    sysctls,
    caps,
    edit,
    id
):
    dclient = docker.from_env()
    if edit == True:
        try:
            dclient.containers.get(id)
            try:
                running_app = dclient.containers.get(id)
                running_app.remove(force=True)
            except Exception as e:
                raise e
        except Exception as e:
            # User probably changed the name so it doesn't conflict. If this is the case we'll just spin up a second container.
            pass

    combined_labels = Merge(portlabels, labels)
    try:
        lauch = dclient.containers.run(
            name=name,
            image=image,
            restart_policy=restart_policy,
            ports=ports,
            network=network,
            network_mode=network_mode,
            volumes=volumes,
            environment=env,
            sysctls=sysctls,
            labels=combined_labels,
            devices=devices,
            cap_add=caps,
            detach=True,
        )
    except Exception as e:
        if e.status_code == 500:
            failed_app = dclient.containers.get(name)
            failed_app.remove()
        raise e

    print(
        f"""Container started successfully.
       Name: {name},
      Image: {image},
      Ports: {ports},
    Volumes: {volumes},
        Env: {env}"""
    )
    return lauch


"""
Runs an app action (ie. docker stop, docker start, etc.)
"""


def app_action(app_name, action):
    err = None
    dclient = docker.from_env()
    app = dclient.containers.get(app_name)
    _action = getattr(app, action)
    if action == "remove":
        try:
            _action(force=True)
        except Exception as exc:
            raise HTTPException(
                status_code=exc.response.status_code, detail=exc.explanation
            )
    else:
        try:
            _action()
        except Exception as exc:
            raise HTTPException(
                status_code=exc.response.status_code, detail=exc.explanation
            )
    apps_list = get_apps()
    return apps_list


"""
Spins up a watchtower container that uses the --run-once
and --cleanup flags and targets a container by name
"""


def app_update(app_name):
    dclient = docker.from_env()
    try:
        old = dclient.containers.get(app_name)
    except Exception as exc:
        print(exc)
        if exc.response.status_code == 404:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail="Unable to get container ID",
            )
        else:
            raise HTTPException(
                status_code=exc.response.status_code, detail=exc.explanation
            )

    volumes = {"/var/run/docker.sock": {"bind": "/var/run/docker.sock", "mode": "rw"}}
    try:
        updater = dclient.containers.run(
            image="containrrr/watchtower:latest",
            command="--cleanup --run-once " + old.name,
            remove=True,
            detach=True,
            volumes=volumes,
        )
    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=exc.response.status_code, detail=exc.explanation
        )

    print("**** Updating " + old.name + "****")
    result = updater.wait(timeout=120)
    print(result)
    time.sleep(1)
    return get_apps()


"""
Checks for current docker id (the one yacht is running
in) and then launches the next function in a 
background task.
"""


def _update_self(background_tasks):
    dclient = docker.from_env()
    bash_command = "head -1 /proc/self/cgroup|cut -d/ -f3"
    yacht_id = (
        subprocess.check_output(["bash", "-c", bash_command]).decode("UTF-8").strip()
    )
    try:
        yacht = dclient.containers.get(yacht_id)
    except Exception as exc:
        print(exc)
        if exc.response.status_code == 404:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail="Unable to get Yacht container ID",
            )
        else:
            status_code = 500
            detail = exc.args[0]
            raise HTTPException(status_code=status_code, detail=detail)
    background_tasks.add_task(update_self_in_background, yacht)
    return {"result": "successful"}


"""
Spins up a watchtower instance with --cleanup and 
--run-once pointed at the current ID of yacht.
"""


def update_self_in_background(yacht):
    dclient = docker.from_env()
    volumes = {"/var/run/docker.sock": {"bind": "/var/run/docker.sock", "mode": "rw"}}
    print("**** Updating " + yacht.name + "****")
    dclient.containers.run(
        image="containrrr/watchtower:latest",
        command="--cleanup --run-once " + yacht.name,
        remove=True,
        detach=True,
        volumes=volumes,
    )


"""
Checks current docker id and compares the repo digest
to the local digest to see if there's an updata available.
"""


def check_self_update():
    dclient = docker.from_env()
    bash_command = "head -1 /proc/self/cgroup|cut -d/ -f3"
    yacht_id = (
        subprocess.check_output(["bash", "-c", bash_command]).decode("UTF-8").strip()
    )
    try:
        yacht = dclient.containers.get(yacht_id)
    except Exception as exc:
        print(exc)
        if hasattr(exc, "response") and exc.response.status_code == 404:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail="Unable to get Yacht container ID",
            )
        elif hasattr(exc, "response"):
            raise HTTPException(
                status_code=exc.response.status_code, detail=exc.explanation
            )
        else:
            raise HTTPException(status_code=400, detail=exc.args)

    return _check_updates(yacht.image.tags[0])
