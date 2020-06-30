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
from app.app_templates.forms import (
    TemplateForm,
    ComposeForm,
)
from app.decorators import admin_required
from app.email import send_email
from app.models import Template, TemplateContent, Compose

import wget
import os  # used for getting file type and deleting files
from urllib.parse import urlparse  # used for getting filetype from url
import urllib.request
import json  # Used for getting template data
import docker


# used to reset the object for later use within the db.session
from sqlalchemy.orm.session import make_transient
from datetime import datetime


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
@login_required
@admin_required
def template_info(template_id):
    """ View template info. """
    template = Template.query.get_or_404(template_id)
    return render_template('app_templates/manage_templates.html', template=template)


@templates.route('/templates/<int:template_id>/content', methods=['GET', 'POST'])
@login_required
@admin_required
def template_content(template_id):
    """ Generate a list of apps associated with the template based on id """
    template = Template.query.get_or_404(template_id)
    apps = TemplateContent.query.join(
        Template, Template.id == TemplateContent.template_id
    ).with_entities(
        TemplateContent.title,
        TemplateContent.logo,
        TemplateContent.description,
        TemplateContent.categories,
        TemplateContent.id
    ).filter(
        TemplateContent.template_id==template_id
    ).order_by(
        TemplateContent.title.asc()
    ).all()
    return render_template('app_templates/manage_templates.html', **locals())

@templates.route('/templates/<int:template_id>/content/<int:app_id>')
@login_required
@admin_required
def template_content_app(template_id, app_id):
    template = Template.query.get_or_404(template_id)
    app = TemplateContent.query.get_or_404(app_id)
    return render_template('app_templates/app_info.html', **locals())



# combine those two using methods GET and POST
@templates.route('/apps/<int:template_id>/delete')
@login_required
@admin_required
def delete_template_request(template_id):
    """Request deletion of a template."""
    template = Template.query.get_or_404(template_id)
    return render_template('app_templates/manage_templates.html', template=template)

# combine those two using methods GET and POST
@templates.route('/apps/<int:template_id>/_delete')
@login_required
@admin_required
def delete_template(template_id):
    """Delete a template."""
    template = Template.query.get_or_404(template_id)
    db.session.delete(template)
    db.session.commit()
    flash('Successfully deleted template.')
    return redirect(url_for('templates.view_templates'))


@templates.route('/new-template', methods=['GET', 'POST'])  # Set URL
@login_required
@admin_required
def new_template():
    """Add a new app template."""
    # Set the form for this page
    form = TemplateForm(request.form)
    if form.validate_on_submit():
        # Check the file type and depending on the file, download it and add it
        # to the db.
        template_name = form.template_name.data
        template_url = form.template_url.data
        template = Template(
            name=template_name,
            url=template_url,
        )
        # Break down template into individual apps and then put their data into
        # the db for later use.
        try:
            # Opens the JSON and iterate over the content.
            with urllib.request.urlopen(template_url) as file:
                for entry in json.load(file):

                    ports = conv_ports2dict(entry.get('ports', []))

                    # Optional use classmethod from_dict
                    template_content = TemplateContent(
                        type=int(entry['type']),
                        title=entry['title'],
                        platform=entry['platform'],
                        description=entry.get('description', ''),
                        name=entry.get('name', entry['title'].lower()),
                        logo=entry.get('logo', ''),
                        image=entry.get('image', ''),
                        notes=entry.get('note', ''),
                        categories=entry.get('categories', ''), # default: '' or []
                        restart_policy=entry.get('restart_policy'),
                        sysctls=entry.get('sysctls'),
                        ports=ports,
                        volumes=entry.get('volumes'),
                        env=entry.get('env'),
                    )
                    template.items.append(template_content)
        except (OSError, TypeError, ValueError) as err:
            # Optional handle KeyError here too.
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


# begin utils.py
# Note: I use a different folder structure in my project.

import re

REGEXP_PORT_ASSIGN = r'^(?:\d{1,5}\:)?\d{1,5}|\:\d{1,5}/(?:tcp|udp)$'

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
def conv_ports2dict(data):
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
            if not cport: cport = None
        hport,proto = hport.split('/', 1)
        portlst.append({ 'cport': cport, 'hport': hport, 'proto': proto })
    return portlst

# endof utils.py


# should be HTTP POST request
@templates.route('/templates/<int:template_id>/refresh')
@login_required
@admin_required
def update(template_id):
    template = Template.query.get_or_404(template_id)
    items = []
    try:
        with urllib.request.urlopen(template.url) as fp:
            for entry in json.load(fp):
                # Optional use classmethod from_dict

                ports = conv_ports2dict(entry.get('ports', []))

                template_content = TemplateContent(
                    type=int(entry['type']),
                    title=entry['title'],
                    platform=entry['platform'],
                    description=entry.get('description', ''),
                    name=entry.get('name', entry['title'].lower()),
                    logo=entry.get('logo', ''),
                    image=entry.get('image', ''),
                    notes=entry.get('note', ''),
                    categories=entry.get('categories', ''), # default: '' or []
                    restart_policy=entry.get('restart_policy'),
                    ports=ports,
                    volumes=entry.get('volumes'),
                    env=entry.get('env'),
                )
                items.append(template_content)
    except Exception as exc:
        # connection problems or incorrect JSON data
        flash('Template update failed')
    else:
        db.session.delete(template)
        db.session.commit()

        make_transient(template)
        template.id = None
        template.updated_at = datetime.utcnow()
        template.items = items

        try:
            db.session.add(template)
            db.session.commit()
            print("Template \"" + template.name + "\" updated successfully.")
        except Exception as exc:
            db.session.rollback()
            raise

    return redirect(url_for('templates.view_templates'))


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
