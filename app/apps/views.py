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
        template_url = form.template_url.data
        flash("added template: " + template_url)
        template_path = urlparse(template_url).path
        ext = os.path.splitext(template_path)[1]
        flash("Extension = " + ext )
        if ext == '.json':
            flash('var = .json')
            template_path = wget.download(template_url, out='app/storage/templates/json')
            flash(template_path)
        elif ext in ('.yml', '.yaml'):
            flash('var = .yaml')
            template_path = wget.download(template_url, out='app/storage/templates/compose')
            flash(template_path)
        
        template = Template(
            name = template_name,
            url = template_url,
            path = template_path,
        )
        db.session.add(template)
        db.session.commit()


        return redirect(url_for('apps.index'))
    return render_template('apps/new_template.html', form=form)