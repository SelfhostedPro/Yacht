from fastapi import HTTPException
from sh import docker_compose
import os
import yaml
import pathlib

from ..settings import Settings
from ..utils.compose import find_yml_files, get_readme_file, get_logo_file

settings = Settings()


def compose_action(name, action):
    files = find_yml_files(settings.COMPOSE_DIR)
    compose = get_compose(name)
    if action == "up":
        try:
            _action = docker_compose(
                "-f",
                compose["path"],
                action,
                "-d",
                _cwd=os.path.dirname(compose["path"]),
            )
        except Exception as exc:
            raise HTTPException(400, exc.stderr.decode("UTF-8").rstrip())
    elif action == "create":
        try:
            _action = docker_compose(
                "-f",
                compose["path"],
                "up",
                "--no-start",
                _cwd=os.path.dirname(compose["path"]),
            )
        except Exception as exc:
            raise HTTPException(400, exc.stderr.decode("UTF-8").rstrip())
    else:
        try:
            _action = docker_compose(
                "-f", compose["path"], action, _cwd=os.path.dirname(compose["path"])
            )
        except Exception as exc:
            raise HTTPException(400, exc.stderr.decode("UTF-8").rstrip())
    if _action.stdout.decode("UTF-8").rstrip():
        output = _action.stdout.decode("UTF-8").rstrip()
    elif _action.stderr.decode("UTF-8").rstrip():
        output = _action.stderr.decode("UTF-8").rstrip()
    else:
        output = "No Output"
    print(f"""Project {compose['name']} {action} successful.""")
    print(f"""Output: """)
    print(output)
    return get_compose_projects()


def compose_app_action(
    name,
    action,
    app,
):
    
    files = find_yml_files(settings.COMPOSE_DIR)
    compose = get_compose(name)
    print('docker-compose -f ' +compose["path"] + ' ' + action + ' ' + app)
    if action == "create":
        try:
            _action = docker_compose(
                "-f",
                compose["path"],
                "up",
                "--no-start",
                app,
                _cwd=os.path.dirname(compose["path"]),
            )
        except Exception as exc:
            raise HTTPException(400, exc.stderr.decode("UTF-8").rstrip())
    elif action == "rm":
        try:
            _action = docker_compose(
                "-f",
                compose["path"],
                "rm",
                "--force",
                app,
                _cwd=os.path.dirname(compose["path"]),
            )
        except Exception as exc:
            raise HTTPException(400, exc.stderr.decode("UTF-8").rstrip())
    else:
        try:
            _action = docker_compose(
                "-f",
                compose["path"],
                action,
                app,
                _cwd=os.path.dirname(compose["path"]),
            )
        except Exception as exc:
            raise HTTPException(400, exc.stderr.decode("UTF-8").rstrip())
    if _action.stdout.decode("UTF-8").rstrip():
        output = _action.stdout.decode("UTF-8").rstrip()
    elif _action.stderr.decode("UTF-8").rstrip():
        output = _action.stderr.decode("UTF-8").rstrip()
    else:
        output = "No Output"
    print(f"""Project {compose['name']} App {name} {action} successful.""")
    print(f"""Output: """)
    print(output)
    return get_compose_projects()


def get_compose_projects():
    files = find_yml_files(settings.COMPOSE_DIR)

    projects = []
    for project, file in files.items():
        volumes = []
        networks = []
        services = {}
        compose = open(file)
        loaded_compose = yaml.load(compose, Loader=yaml.SafeLoader)
        if loaded_compose.get("volumes"):
            for volume in loaded_compose.get("volumes"):
                volumes.append(volume)
        if loaded_compose.get("networks"):
            for network in loaded_compose.get("networks"):
                networks.append(network)
        for service in loaded_compose.get("services"):
            services[service] = loaded_compose["services"][service]
        _project = {
            "name": project,
            "path": file,
            "version": loaded_compose["version"],
            "services": services,
            "volumes": volumes,
            "networks": networks,
        }
        projects.append(_project)
    return projects


def get_compose(name):
    try:
        files = find_yml_files(settings.COMPOSE_DIR + name)
    except Exception as exc:
        print(exc)
    for project, file in files.items():
        if name == project:
            networks = []
            volumes = []
            services = {}
            compose = open(file)
            loaded_compose = yaml.load(compose, Loader=yaml.SafeLoader)
            if loaded_compose.get("volumes"):
                for volume in loaded_compose.get("volumes"):
                    volumes.append(volume)
            if loaded_compose.get("networks"):
                for network in loaded_compose.get("networks"):
                    networks.append(network)
            for service in loaded_compose.get("services"):
                services[service] = loaded_compose["services"][service]
            compose_object = {
                "name": project,
                "path": file,
                "version": loaded_compose["version"],
                "services": services,
                "volumes": volumes,
                "networks": networks,
            }
            return compose_object
    else:
        raise HTTPException(404, "Project " + name + " not found")


def write_compose(compose):
    print(compose)
    pathlib.Path("config/compose/" + compose.name).mkdir(parents=True)
    f = open("config/compose/" + compose.name + "/docker-compose.yml", "a")
    f.write(compose.content)
    f.close()

    return get_compose(name=compose.name)