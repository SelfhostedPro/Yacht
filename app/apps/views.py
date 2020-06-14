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
    ChangeAccountTypeForm,
    ChangeUserEmailForm,
    InviteUserForm,
    TemplateForm,
)
from app.decorators import admin_required
from app.email import send_email
from app.models import EditableHTML, Role, User

import os #used for getting file type
from urllib.parse import urlparse
import wget

apps = Blueprint('apps', __name__)


@apps.route('/')
@login_required
@admin_required
def index():
    """Apps dashboard page."""
    return render_template('apps/index.html')

@apps.route('/new-template', methods=['GET', 'POST'])
@login_required
@admin_required
def new_template():
    """Add a new app template."""
    form = TemplateForm(request.form)
    
    if form.validate_on_submit():
        template_name = form.template_name.data
        template_location = form.template_url.data
        flash("added template: " + template_location)
        template_path = urlparse(template_location).path
        ext = os.path.splitext(template_path)[1]
        flash("Extension = " + ext )
        if ext == '.json':
            flash('var = .json')
            template_filename = wget.download(template_location, out='app/storage/templates/json')
            flash(template_filename)
        elif ext in ('.yml', '.yaml'):
            flash('var = .yaml')
            template_filename = wget.download(template_location, out='app/storage/templates/compose')
            flash(template_filename)
        
        template = Template(
            name = template_name,
            url = template_location,
            path = template_filename,
        )
        db.session.add(template)
        db.session.commit()
        flash('Template {} successfully created'.format(template.name()), 'form-success')

        return redirect(url_for('apps.index'))
    return render_template('apps/new_template.html', form=form)