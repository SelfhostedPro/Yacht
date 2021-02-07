from fastapi import HTTPException
from sh import docker_compose
import os
import yaml
import pathlib
import shutil

from ..settings import Settings
from ..utils.compose import find_yml_files, get_readme_file, get_logo_file

settings = Settings()


def compose_action(name, action):
    files = find_yml_files(settings.COMPOSE_DIR)
    compose = get_compose(name)
    if action == "up":
        try:
            _action = docker_compose(
                action,
                "-d",
                _cwd=os.path.dirname(compose["path"]),
                _env={'clear_env': 'true'}
            )
        except Exception as exc:
            raise HTTPException(400, exc.stderr.decode("UTF-8").rstrip())
    elif action == "create":
        try:
            _action = docker_compose(
                "up",
                "--no-start",
                _cwd=os.path.dirname(compose["path"]),
                _env={'clear_env': 'true'}
            )
        except Exception as exc:
            raise HTTPException(400, exc.stderr.decode("UTF-8").rstrip())
    else:
        try:
            _action = docker_compose(
                action, _cwd=os.path.dirname(compose["path"]),_env={'clear_env': 'true'}
            )
        except Exception as exc:
            print(exc)
            raise HTTPException(400, exc.stderr.decode("UTF-8").rstrip())
    if _action.stdout.decode("UTF-8").rstrip():
        _output = _action.stdout.decode("UTF-8").rstrip()
    elif _action.stderr.decode("UTF-8").rstrip():
        _output = _action.stderr.decode("UTF-8").rstrip()
    else:
        _output = "No Output"
    print(f"""Project {compose['name']} {action} successful.""")
    print(f"""Output: """)
    print(_output)
    return get_compose_projects()


def compose_app_action(
    name,
    action,
    app,
):

    files = find_yml_files(settings.COMPOSE_DIR)
    compose = get_compose(name)
    print("docker-compose -f " + compose["path"] + " " + action + " " + app)
    if action == "up":
        try:
            _action = docker_compose(
                "up",
                "-d",
                app,
                _cwd=os.path.dirname(compose["path"]),
                _env={'clear_env': 'true'}
            )
        except Exception as exc:
            raise HTTPException(400, exc.stderr.decode("UTF-8").rstrip())
    elif action == "create":
        try:
            _action = docker_compose(
                "up",
                "--no-start",
                app,
                _cwd=os.path.dirname(compose["path"]),
                _env={'clear_env': 'true'}
            )
        except Exception as exc:
            raise HTTPException(400, exc.stderr.decode("UTF-8").rstrip())
    elif action == "rm":
        try:
            _action = docker_compose(
                "rm",
                "--force",
                "--stop",
                app,
                _cwd=os.path.dirname(compose["path"]),
                _env={'clear_env': 'true'}
            )
        except Exception as exc:
            raise HTTPException(400, exc.stderr.decode("UTF-8").rstrip())
    else:
        try:
            _action = docker_compose(
                action,
                app,
                _cwd=os.path.dirname(compose["path"]),
                _env={'clear_env': 'true'}
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
        if loaded_compose:
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
                "version": loaded_compose.get("version", "3.9"),
                "services": services,
                "volumes": volumes,
                "networks": networks,
            }
            projects.append(_project)
        else:
            print("ERROR: " + file + " is invalid or empty!")
    return projects


def get_compose(name):
    try:
        files = find_yml_files(settings.COMPOSE_DIR + name)
    except Exception as exc:
        raise HTTPException(exc.status_code, exc.detail)
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
            _content = open(file)
            content = _content.read()
            compose_object = {
                "name": project,
                "path": file,
                "version": loaded_compose.get("version", '-'),
                "services": services,
                "volumes": volumes,
                "networks": networks,
                "content": content,
            }
            return compose_object
    else:
        raise HTTPException(404, "Project " + name + " not found")


def write_compose(compose):
    if not os.path.exists(settings.COMPOSE_DIR + compose.name):
        try:
            pathlib.Path(settings.COMPOSE_DIR + compose.name).mkdir(parents=True)
        except Exception as exc:
            raise HTTPException(exc.status_code, exc.detail)
    with open(settings.COMPOSE_DIR + compose.name + "/docker-compose.yml", "w") as f:
        try:
            f.write(compose.content)
            f.close()
        except Exception as exc:
            raise HTTPException(exc.status_code, exc.detail)

    return get_compose(name=compose.name)

def delete_compose(project_name):
    if not os.path.exists('/'+settings.COMPOSE_DIR+project_name):
        raise HTTPException(404, "Project directory not found.")
    elif not os.path.exists('/'+settings.COMPOSE_DIR + project_name+"/docker-compose.yml"):
        raise HTTPException(404, "Project docker-compose.yml not found.")
    else:
        try:
            with open('/'+settings.COMPOSE_DIR + project_name + '/docker-compose.yml'):
                pass
        except OSError as exc:
            raise HTTPException(400,exc.strerror)
    try:
        shutil.rmtree('/'+settings.COMPOSE_DIR+project_name)
    except Exception as exc:
        raise HTTPException(exc.status_code, exc.strerror)
    return get_compose_projects()
