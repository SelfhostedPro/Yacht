from fastapi import HTTPException
from sh import docker_compose
import yaml

from ..settings import Settings
from ..utils.compose import find_yml_files, get_readme_file, get_logo_file

settings=Settings()

def compose_action(name, action):
    files = find_yml_files(settings.COMPOSE_DIR)
    for project, file in files.items():
        if name == project:
            path = file
            if action == "up":
                try:
                    _action = docker_compose("-f", path, action, '-d')
                except Exception as exc:
                    raise HTTPException(400, exc.stderr.decode('UTF-8').rstrip())
            else:
                _action = docker_compose("-f", path, action)
            break
    else:
        raise HTTPException(404, 'Project not found.')
    if _action.stdout.decode('UTF-8').rstrip():
        output = _action.stdout.decode('UTF-8').rstrip()
    elif _action.stderr.decode('UTF-8').rstrip():
        output = _action.stderr.decode('UTF-8').rstrip()
    else:
        output = 'No Output'
    return {'success': True, 'project': project, 'action': action, 'output': output}

def get_compose_projects():
    files = find_yml_files(settings.COMPOSE_DIR)

    projects = []
    for project, file in files.items():
        volumes = []
        networks = []
        services = {}
        compose = open(file)
        loaded_compose = yaml.load(compose, Loader=yaml.SafeLoader)
        if loaded_compose.get('volumes'):
            for volume in loaded_compose.get('volumes'):
                volumes.append(volume)
        if loaded_compose.get('networks'):
            for network in loaded_compose.get('networks'):
                networks.append(network)
        for service in loaded_compose.get('services'):
            services[service] = loaded_compose['services'][service]
        _project = {'name': project, 'path': file, 'version': loaded_compose['version'], 'services': services, 'volumes': volumes, "networks": networks}
        projects.append(_project)
    return projects