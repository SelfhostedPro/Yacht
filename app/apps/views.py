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
    _PortForm,
    _SysctlsForm
)
from app.decorators import admin_required
from app.email import send_email
from app.models import Template, TemplateContent, Compose

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
    apps = TemplateContent.query.all()
    return render_template('apps/add_app.html', apps=apps)


@apps.route('/add/<app_id>/')
@apps.route('/add/<app_id>/info', methods=['GET', 'POST'])
@login_required
@admin_required
def deploy_app(app_id):
    """ Form to deploy an app """
    app = TemplateContent.query.get_or_404(app_id)
    if app.sysctls and 'name' not in app.sysctls[0]:
        app.sysctls = conv_ctls2form(app.sysctls)
    form = DeployForm(request.form, obj=app)
    if form.validate_on_submit():
        print('valid')
        try:
            launch_container(
                form.name.data,
                form.image.data,
                conv_ports2data(form.ports.data),
                conv_volumes2data(form.volumes.data),
                conv_env2data(form.env.data),
                conv_sysctls2data(form.sysctls.data))
        except Exception as exc: raise
        print('stop')
        return redirect(url_for('apps.index'))

    # only for debugging!
    # for fieldName, errorMessages in form.errors.items():
    #     for err in errorMessages:
    #         print(f'{fieldName}: {err}')

    return render_template('apps/deploy_app.html', **locals())

# begin utils.py
# Note: I use a different folder structure in my project.

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

# Input Format:
# [{"sysctl_name": "sysctl_value"}]
# Result Format:
#
# {"sysctl_name": "sysctl_value"}
def conv_ctls2form(data):
    if not all(isinstance(x, dict) for x in data):
        raise TypeError('Expected list of str types.')

    return [{'name':k,'value':v} for d in data for k,v in d.items()]

def conv_sysctls2data(data):
    if data:
        return dict((d['name'], d['value']) for d in data)
    else:
        sysctls = None
        return sysctls

def launch_container(name, image, ports, volumes, env, sysctls):
    dclient = docker.from_env()
    dclient.containers.run(
        name=name,
        image=image,
        volumes=volumes,
        environment=env,
        ports=ports,
        sysctls=sysctls,
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
