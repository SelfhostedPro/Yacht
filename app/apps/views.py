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
    """Add a new app."""
    form = TemplateForm()
    if form.validate_on_submit():
        return redirect(url_for('apps.index'))
    return render_template('apps/new_template.html', form=form)