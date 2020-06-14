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
)
from app.decorators import admin_required
from app.email import send_email
from app.models import Template

import os #used for getting file type and deleting files
from urllib.parse import urlparse #used for getting filetype from url
import wget #used to download file

apps = Blueprint('apps', __name__)


@apps.route('/')
@login_required
@admin_required
def index():
    """Apps dashboard page."""
    return render_template('apps/index.html')

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
    print(template)
    filepath = template.path
    print(filepath)
    with open(filepath, 'r') as f:
        return render_template('apps/manage_templates.html', template=template, content=f.read())

@apps.route('/new-template', methods=['GET', 'POST']) #Set URL
@login_required
@admin_required #Require admin permissions
def new_template():
    """Add a new app template."""
    form = TemplateForm(request.form) #Set the form for this page
    
    if form.validate_on_submit():
        #Check the file type and depending on the file, download it and add it to the db.
        template_name = form.template_name.data
        template_url = form.template_url.data #Set var for template_url
        flash("added template: " + template_url)
        template_path = urlparse(template_url).path #Get the file path
        ext = os.path.splitext(template_path)[1]    #Get the file extension
        flash("Extension = " + ext )
        if ext == '.json':
            flash('var = .json')
            template_path = wget.download(template_url, out='app/storage/templates/json')
            flash(template_path)
        elif ext in ('.yml', '.yaml'):
            flash('var = .yaml')
            template_path = wget.download(template_url, out='app/storage/templates/compose')
            flash(template_path)
        #Add the template to the database with basic info
        template = Template(
            name = template_name,
            url = template_url,
            path = template_path,
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
    return render_template('apps/new_template.html', form=form)