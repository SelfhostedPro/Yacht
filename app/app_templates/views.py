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
from app.app_templates.forms import (
    TemplateForm,
    ComposeForm,
)
from app.decorators import admin_required
from app.email import send_email
from app.models import Template, Template_Content, Compose

import wget
import os  # used for getting file type and deleting files
from urllib.parse import urlparse  # used for getting filetype from url
import urllib.request
import json  # Used for getting template data
import docker

templates = Blueprint('templates', __name__)


@templates.route('/')
@login_required
@admin_required
def index():
    """Apps dashboard page."""
    return render_template('app_templates/index.html')


@templates.route('/view')
@login_required
@admin_required
def view_templates():
    """ View all templates """
    template = Template.query.all()
    return render_template('app_templates/view_templates.html', template=template)


@templates.route('/templates/<int:template_id>')
@templates.route('/templates/<int:template_id>/info')
def template_info(template_id):
    """ View template info. """
    template = Template.query.filter_by(id=template_id).first()
    if template is None:
        abort(404)
    return render_template('app_templates/manage_templates.html', template=template)


@templates.route('/templates/<int:template_id>/content', methods=['GET', 'POST'])
@login_required
@admin_required
def template_content(template_id):
    """ Generate a list of apps associated with the template based on id """
    template = Template.query.filter_by(id=template_id).first()
    template_list = Template_Content.query.filter_by(
        template_id=template_id).all()
    app_names = []
    app_logos = []
    for n in template_list:
        app_names.append(n.title)
    for l in template_list:
        app_logos.append(l.logo)
    # Combine the names and urls into a turple in order to refrence them together in a list
    apps = tuple(zip(app_names, app_logos))
    sorted_apps = sorted(apps)
    print(apps)
    return render_template('app_templates/manage_templates.html', template=template, apps=sorted_apps)


@templates.route('/apps/<int:template_id>/delete')
@login_required
@admin_required
def delete_template_request(template_id):
    """Request deletion of a template."""
    template = Template.query.filter_by(id=template_id).first()
    if template is None:
        abort(404)
    return render_template('app_templates/manage_templates.html', template=template)


@templates.route('/apps/<int:template_id>/_delete')
@login_required
@admin_required
def delete_template(template_id):
    """Delete a template."""
    template = Template.query.filter_by(id=template_id).first()
    db.session.delete(template)
    db.session.commit()
    flash('Successfully deleted template.')
    return redirect(url_for('templates.view_templates'))


@templates.route('/new-template', methods=['GET', 'POST'])  # Set URL
@login_required
@admin_required
def new_template():
    """Add a new app template."""
    form = TemplateForm(request.form)  # Set the form for this page

    if form.validate_on_submit():
        # Check the file type and depending on the file, download it and add it to the db.
        template_name = form.template_name.data
        template_url = form.template_url.data
        template = Template(
            name=template_name,
            url=template_url,
        )
        try:
            # Break down template into individual apps and then put their data into the db for later use
            for f in fetch_json(template_url):
                template_content = Template_Content(
                    type=f.get('type'),
                    title=f.get('title'),
                    name=f.get('name'),
                    notes=f.get('notes'),
                    description=f.get('description'),
                    logo=f.get('logo'),
                    image=f.get('image'),
                    categories=f.get('categories'),
                    platform=f.get('platform'),
                    restart_policy=f.get('restart_policy'),
                    ports=f.get('ports'),
                    volumes=f.get('volumes'),
                    env=f.get('env'),
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

        return redirect(url_for('templates.index'))
    return render_template('app_templates/new_template.html', form=form)


def fetch_json(template_url):  # Opens the JSON template for use in the above route
    with urllib.request.urlopen(template_url) as file:
        return json.load(file)

# Below section is not in use yet


@templates.route('/new-compose', methods=['GET', 'POST'])  # Set URL
@login_required
@admin_required  # Require admin permissions
def new_compose():
    """Add a new app template."""
    form = ComposeForm(request.form)  # Set the form for this page

    if form.validate_on_submit():
        # Check the file type and depending on the file, download it and add it to the db.
        template_name = form.template_name.data
        template_url = form.template_url.data  # Set var for template_url
        description = form.description
        flash("added template: " + template_url)
        template_path = urlparse(template_url).path  # Get the file path
        ext = os.path.splitext(template_path)[1]  # Get the file extension
        flash("Extension = " + ext)

        if ext in ('.yml', '.yaml'):
            flash('var = .yaml')
            template_path = wget.download(
                template_url, out='app/storage/templates/compose')
            flash(template_path)
        # Add the template to the database with basic info
        template = Compose(
            name=template_name,
            url=template_url,
            path=template_path,
            description=description
        )
        try:
            db.session.add(template)  # try to commit to the db
            db.session.commit()
        except:
            # if there's an error rollback and delete the file.
            db.session.rollback()
            if os.path.exists(template_path):
                os.remove(template_path)
            else:
                flash("File download failed")

        return redirect(url_for('templates.index'))
    return render_template('app_templates/new_compose.html', form=form)
