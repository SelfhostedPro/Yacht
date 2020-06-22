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
from flask_rq import get_queue

from app import db
from app.apps.forms import (
    DeployForm,
    _VolumeForm,
    _EnvForm
)
from app.decorators import admin_required
from app.email import send_email
from app.models import Template, Template_Content, Compose

import os #used for getting file type and deleting files
from urllib.parse import urlparse #used for getting filetype from url
import urllib.request, json #Used for getting template data
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
    app = Template_Content.query.filter_by(id=app_id).first()
    form = DeployForm(request.form, obj=app) #Set the form for this page
    volumes = app.volumes
    ports = app.ports
    env = app.env


    if form.validate_on_submit():
        print('valid')
        if form.env.data:
            env = transform_env_data(form)
        if form.ports.data:
            ports = transform_port_data(form)
        if form.volumes.data:
            volumes = transform_volume_data(form)
        print('stop')
        launch_container(form, volumes, ports, env)
        return redirect(url_for('apps.index'))
    return render_template('apps/deploy_app.html', **locals())

def transform_volume_data(form):
    devices_dict = {}
    for volume_data in form.volumes.data:
        devices_dict.update({ volume_data['bind']: { 'bind': volume_data['container'], 'mode': 'rw'}})
    return devices_dict

def transform_port_data(form):
    port_list = []
    for port_data in form.ports.data:
        separator = ':'
        port_list.append(port_data.split(separator))
    port_dict = {i[0]:i[1] for i in port_list}
    print(port_dict)
    return port_dict

def transform_env_data(form):
    env_list = []
    for env_data in form.env.data:
        separator = '='
        env_list.append(separator.join(env_data.values()))
    print(env_list)
    return env_list

def launch_container(form, volumes, ports, env):
    dclient = docker.from_env()
    dclient.containers.run(
        name = form.name.data,
        image = form.image.data,
        volumes = volumes,
        environment = env,
        ports = ports,
        restart_policy = {"Name": 'unless-stopped'},
        detach = True
    )
    print("something")
    return

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
def container_info(container_name):
    """ View container info """
    dclient = docker.from_env()
    container = dclient.containers.get(container_name)
    return render_template('apps/manage_app.html', container=container)

# @templates.route('/templates/<int:template_id>')
# @templates.route('/templates/<int:template_id>/info')
# def template_info(template_id):
#     """ View template info. """
#     template = Template.query.filter_by(id=template_id).first()
#     if template is None:
#         abort(404)
#     return render_template('app_templates/manage_templates.html', template=template)