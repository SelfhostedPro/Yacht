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
    TemplateForm,
    ComposeForm,
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
@apps.route('/view')
@login_required
@admin_required
def running_apps():
    """ View all apps """
    client = docker.from_env()
    apps = client.containers.list()
    return render_template('apps/view_apps.html', apps=apps)

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
    client = docker.from_env()
    client.containers.run(
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

@apps.route('/templates')
@login_required
@admin_required
def view_templates():
    """ View all templates """
    template = Template.query.all()
    return render_template('apps/view_templates.html', template=template)

@apps.route('/templates/<int:template_id>')
@apps.route('/templates/<int:template_id>/info')
def template_info(template_id):
    """ View template info. """
    template = Template.query.filter_by(id=template_id).first()
    if template is None:
        abort(404)
    return render_template('apps/manage_templates.html', template=template)

@apps.route('/templates/<int:template_id>/content', methods=['GET', 'POST'])
@login_required
@admin_required
def template_content(template_id):
    """ Generate a list of apps associated with the template based on id """
    template = Template.query.filter_by(id=template_id).first()
    template_list = Template_Content.query.filter_by(template_id=template_id).all()
    app_names = []
    app_logos = []
    for n in template_list:
        app_names.append(n.title)
    for l in template_list:
        app_logos.append(l.logo)
    apps = tuple(zip(app_names,app_logos)) #Combine the names and urls into a turple in order to refrence them together in a list
    print(apps)
    return render_template('apps/manage_templates.html', template=template, apps=apps)

@apps.route('/apps/<int:template_id>/delete')
@login_required
@admin_required
def delete_template_request(template_id):
    """Request deletion of a template."""
    template = Template.query.filter_by(id=template_id).first()
    if template is None:
        abort(404)
    return render_template('apps/manage_templates.html', template=template)

@apps.route('/apps/<int:template_id>/_delete')
@login_required
@admin_required
def delete_template(template_id):
    """Delete a template."""
    template = Template.query.filter_by(id=template_id).first()
    db.session.delete(template)
    db.session.commit()
    flash('Successfully deleted template.')
    return redirect(url_for('apps.view_templates'))

@apps.route('/new-template', methods=['GET', 'POST']) #Set URL
@login_required
@admin_required
def new_template():
    """Add a new app template."""
    form = TemplateForm(request.form) #Set the form for this page
    
    if form.validate_on_submit():
        #Check the file type and depending on the file, download it and add it to the db.
        template_name = form.template_name.data
        template_url = form.template_url.data
        template = Template(
            name = template_name,
            url = template_url,
        )
        try:
            for f in fetch_json(template_url): #Break down template into individual apps and then put their data into the db for later use
                template_content = Template_Content(
                    type = f.get('type'),
                    title = f.get('title'),
                    name = f.get('name'),
                    notes = f.get('notes'),
                    description = f.get('description'),
                    logo = f.get('logo'),
                    image = f.get('image'),
                    categories = f.get('categories'),
                    platform = f.get('platform'),
                    restart_policy = f.get('restart_policy'),
                    ports = f.get('ports'),
                    volumes = f.get('volumes'),
                    env = f.get('env'),
                )
                template.items.append(template_content)
        except OSError as err:
            print('data request failed', err)
            raise
        try: 
            db.session.add(template)
            db.session.commit()
        except SQLAlchemyError as err:
            print('database transaction failed')
            db.session.rollback()
            raise


        return redirect(url_for('apps.index'))
    return render_template('apps/new_template.html', form=form)

def fetch_json(template_url): #Opens the JSON template for use in the above route
    with urllib.request.urlopen(template_url) as file:
        return json.load(file)

###Below section is not in use yet
@apps.route('/new-compose', methods=['GET', 'POST']) #Set URL
@login_required
@admin_required #Require admin permissions
def new_compose():
    """Add a new app template."""
    form = ComposeForm(request.form) #Set the form for this page
    
    if form.validate_on_submit():
        #Check the file type and depending on the file, download it and add it to the db.
        template_name = form.template_name.data
        template_url = form.template_url.data #Set var for template_url
        description = form.description
        flash("added template: " + template_url)
        template_path = urlparse(template_url).path #Get the file path
        ext = os.path.splitext(template_path)[1]    #Get the file extension
        flash("Extension = " + ext )

        if ext in ('.yml', '.yaml'):
            flash('var = .yaml')
            template_path = wget.download(template_url, out='app/storage/templates/compose')
            flash(template_path)
        #Add the template to the database with basic info
        template = Compose(
            name = template_name,
            url = template_url,
            path = template_path,
            description = description
        )
        try:
            db.session.add(template) #try to commit to the db
            db.session.commit()
        except: 
            db.session.rollback() #if there's an error rollback and delete the file.
            if os.path.exists(template_path):
                os.remove(template_path)
            else:
                flash("File download failed")


        return redirect(url_for('apps.index'))
    return render_template('apps/new_compose.html', form=form)