from .. import db
from ..models.containers import (
    Template,
    TemplateItem
)
from ..models.container_schemes import (
    TemplateItemSchema,
    DeploySchema
)

from flask import Blueprint
from flask import (
    abort,
    jsonify,
    make_response,
    request
)
from flask_jwt_extended import (
    jwt_required,
    jwt_optional
)

from webargs import fields, validate
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from webargs.flaskparser import use_args, use_kwargs
from werkzeug.exceptions import MethodNotAllowed, UnprocessableEntity

import os  # used for getting file type and deleting files
from urllib.parse import urlparse  # used for getting filetype from url
import urllib.request
import json  # Used for getting template data
import docker

apps = Blueprint('apps', __name__)

@apps.route('/')
def index():
    apps_list = []
    dclient = docker.from_env()
    apps = dclient.containers.list(all=True)
    for app in apps:
        apps_list.append(app.attrs)
    data = apps_list
    return jsonify({ 'data': data })

@apps.route('/<int:id>')
def list_apps(id):
    try:
        template_item = TemplateItem.query.get_or_404(id)
        template_item_schema = TemplateItemSchema()
        data = template_item_schema.dump(template_item)
        return jsonify({ 'data': data })
    except IntegrityError as err:
        abort(400)


@apps.route('/<int:id>/deploy', methods=['POST'])
@use_args(DeploySchema(), location='json')
def deploy(args, id):
    '''curl -H "Content-Type: application/json" -X POST \
    -d '{"title":"Untitled", "image":"my:image", "ports":[{"proto": "tcp", "hport":2020}]}' \
    http://127.0.0.1:5000/api/apps/1/deploy
    '''
    print(args, id)
    try:
        launch_app(
        args.get('name'),
        args.get('image'),
        conv_restart2data(args.get('restart_policy')),
        conv_ports2data(args.get('ports')),
        conv_volumes2data(args.get('volumes')),
        conv_env2data(args.get('env')),
        conv_sysctls2data(args.get('sysctls')),
        conv_caps2data(args.get('cap_add')))
    except Exception as exc: raise
    print('done deploying')
    # print(id, title, image)
    # print(args, kwargs)
    return jsonify(data = '')

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
#     '53/udp': ('0.0.0.0', 53),
#     '67/udp': ('0.0.0.0', 67),
#     '80/tcp': ('0.0.0.0', 1010),
#     '443/tcp': ('0.0.0.0', 4443)
# }
def conv_ports2data(data):
    ports = {}
    for d in data:
        cport = d.get('cport')
        hport = d.get('hport')
        proto = d.get('proto')
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
    return dict((d['bind'], {'bind': d['container'], 'mode': 'rw'}) for d in data)

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
    return [delim.join((d['name'], d['default'])) for d in data]

def conv_sysctls2data(data):
    if data:
        return dict((d['name'], d['value']) for d in data)
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

def launch_app(name, image, restart_policy, ports, volumes, env, sysctls, caps):
    dclient = docker.from_env()
    dclient.containers.run(
        name=name,
        image=image,
        restart_policy=restart_policy,
        ports=ports,
        volumes=volumes,
        environment=env,
        sysctls=sysctls,
        cap_add=caps
    )
    print(f'''Container started successfully.
       Name: {name},
      Image: {image},
      Ports: {ports},
    Volumes: {volumes},
        Env: {env}''')
    return

@apps.route('/<container_name>/<action>')
def app_actions(container_name, action):
    err = None
    apps_list = []
    dclient = docker.from_env()
    container = dclient.containers.get(container_name)
    # _action = action + '()'
    _action = getattr(container, action)
    if action == 'remove':
        try:
          _action(force=True)
        except Exception as exc:
            err = f"{exc}"
    else:
        try: 
          _action()
        except Exception as exc:
            err = exc.explanation
    
    apps = dclient.containers.list(all=True)
    for app in apps:
        apps_list.append(app.attrs)
    data = apps_list
    return jsonify({ 'data': data, 'error': err })

@apps.route('/<container_name>')
def app_details(container_name):
    container_info= []
    dclient = docker.from_env()
    container = dclient.containers.get(container_name)

    
    data = container.attrs
    print(jsonify({ 'data': data }))
    return jsonify({ 'data': data })



    #     apps_list = []
    # dclient = docker.from_env()
    # apps = dclient.containers.list(all=True)
    # for app in apps:
    #     apps_list.append(app.attrs)
    # data = apps_list
    # return jsonify({ 'data': data })
