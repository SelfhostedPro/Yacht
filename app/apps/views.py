from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required

from app import db
from app.apps.forms import (
    DeployForm,
    _VolumeForm,
    _EnvForm,
    _PortForm
)
from app.decorators import admin_required
from app.email import send_email
from app.models import Template, Template_Content, Compose

import os  # used for getting file type and deleting files
from urllib.parse import urlparse  # used for getting filetype from url
import urllib.request
import json  # Used for getting template data
import docker

apps = Blueprint('apps', __name__)

@apps.route('/')
@login_required
@admin_required
def index():
    """Apps dashboard page."""
    return render_template('apps/index.html')


@apps.route('/add')
@login_required
@admin_required
def view_apps():
    """ View available apps """
    apps = Template_Content.query.all()
    return render_template('apps/add_app.html', apps=apps)


@apps.route('/add/<app_id>/')
@apps.route('/add/<app_id>/info', methods=['GET', 'POST'])
@login_required
@admin_required
def deploy_app(app_id):
    """ Form to deploy an app """
    app = Template_Content.query.get_or_404(app_id)
    form = DeployForm(request.form, obj=app)  # Set the form for this page

    # only in request.method == 'GET' or not form.is_submitted()
    if not form.is_submitted():
        # Reformat the loaded template during the migration of apps.
        # Move this code to app_templates/views/new_template to
        # validate and customize template. [conv_ports2dict(...)]
        try: app.ports = conv_ports2form(app.ports)
        except (TypeError, ValueError) as err: raise

    if form.validate_on_submit():
        print('valid')
        try:
            launch_container(
                form.name.data,
                form.image.data,
                conv_ports2data(form.ports.data),
                conv_volumes2data(form.volumes.data),
                conv_env2data(form.env.data))
        except Exception as exc: raise
        print('stop')
        return redirect(url_for('apps.index'))

    return render_template('apps/deploy_app.html', **locals())

# begin utils.py
# Note: I use a different folder structure in my project.

import re

REGEXP_PORT_ASSIGN = r'^(?:\d{1,5}\:)?\d{1,5}/(?:tcp|udp)$'

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
def conv_ports2form(data):
    if not all(isinstance(x, str) for x in data):
        raise TypeError('Expected list or str types.')
    if not all(re.match(REGEXP_PORT_ASSIGN, x, flags=re.IGNORECASE) for x in data):
        raise ValueError('Malformed port assignment.')

    delim = ':'
    portlst = []
    for port_data in data:
        cport,hport = None,port_data
        if delim in hport:
            cport,hport = hport.split(delim, 1)
        hport,proto = hport.split('/', 1)
        portlst.append({ 'cport': cport, 'hport': hport, 'proto': proto })
    return portlst

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
        cport,hport,proto = d.values()
        if not cport: cport = None
        ports['/'.join((str(hport), proto))] = ('0.0.0.0', cport)
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
#         'label': 'SOMEVARIABLE',
#         'name': None,
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

def launch_container(name, image, ports, volumes, env):
    dclient = docker.from_env()
    dclient.containers.run(
        name=name,
        image=image,
        volumes=volumes,
        environment=env,
        ports=ports,
        restart_policy={"Name": 'unless-stopped'},
        detach=True
    )
    print(f'''Container started successfully.
       Name: {name},
      Image: {image},
      Ports: {ports},
    Volumes: {volumes},
        Env: {env}''')
    return

# endof utils.py

@apps.route('/view')
@login_required
@admin_required
def running_apps():
    """ View all apps """
    dclient = docker.from_env()
    apps = dclient.containers.list(all=True)
    return render_template('apps/view_apps.html', apps=apps)


@apps.route('/view/<container_name>')
@apps.route('/view/<container_name>/info')
@login_required
@admin_required
def container_info(container_name):
    """ View container info """
    dclient = docker.from_env()
    container = dclient.containers.get(container_name)
    return render_template('apps/manage_app.html', container=container)


@apps.route('/view/<container_name>/<action>')
@login_required
@admin_required
def container_actions(container_name, action):
    """ Do an action on a container """
    dclient = docker.from_env()
    container = dclient.containers.get(container_name)
    print(action)
    if action == 'start':
        container.start()
    elif action == 'stop':
        container.stop()
    elif action == 'restart':
        container.restart()
    elif action == 'kill':
        container.kill()
    elif action == 'remove':
        container.remove(force=True)
        return redirect(url_for('apps.view_apps'))
    else:
        print('else')

    return render_template('apps/manage_app.html', container=container)
