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
    DeployForm
)
from app.decorators import admin_required
from app.email import send_email
from app.models import Template, Template_Content, Compose

import os #used for getting file type and deleting files
from urllib.parse import urlparse #used for getting filetype from url
import urllib.request, json

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
    template = Template.query.all()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    json_content = load_json()
    print(len(json_content))
    return render_template('apps/add_app.html', apps=json_content)

def combine_json_templates():

    master_list = []

    cwd = os.getcwd()
    print(cwd)
    json_storage = 'app/storage/templates/json/'


    for file in os.listdir(json_storage):
        with open(json_storage + file) as json_path:
            json_content = json.load(json_path)
            for item in json_content:
                master_list.append(item)
            

    return master_list

def load_json():
    data = []
    json_storage = 'app/storage/templates/json/'
    for fname in glob(os.path.join(json_storage, '*.json')):
        with open(fname) as fp:
            bname,_ = os.path.splitext(os.path.basename(fname))
            dataset = json.load(fp)
            for i,entry in enumerate(dataset):
                entry['uuid']=f'{bname}-{i}'
                data.append(entry)
    return data

@apps.route('/add/<app_id>/')
@apps.route('/add/<app_id>/info', methods=['GET', 'POST'])
@login_required
@admin_required
def app_info(app_id):
    if request.method == 'POST':
        print(app_id)
        a = request.form['ident']
        print(a)
        """Deploy an App"""
        form.container_name.data = a.name
        form.container_image.data = a.image
        form.restart_policy.data = a.restart_policy
        if a.ports:
            form.container_ports.data = a.ports
        if a.volumes:
            form.container_volumes.data = a.volumes
        if a.env:
            form.container_env = a.env
    
    form = DeployForm(request.form) #Set the form for this page
    if form.validate_on_submit():
        container_name = form.name.data
        container_image = form.image.data
        if form.ports.data:
            container_ports = form.ports.data
        if form.volumes.data:
            form.container_volumes.data = volumes
        if form.env.data:
            form.container_env.data = env
        form.restart_policy.data = restart_policy

    
    return render_template('apps/deploy_app.html', form=form)




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
def template_content(template_id,):
    template = Template.query.filter_by(id=template_id).first()
    template_list = Template_Content.query.filter_by(template_id=template_id).all()
    app_names = []
    for n in template_list:
        app_names.append(n.name)

    print(app_names)
    return render_template('apps/manage_templates.html', template=template, content=app_names)

@apps.route('/new-template', methods=['GET', 'POST']) #Set URL
@login_required
@admin_required #Require admin permissions
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
            for f in fetch_json(template_url):
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

def fetch_json(template_url):
    with urllib.request.urlopen(template_url) as file:
        return json.load(file)


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