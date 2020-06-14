from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.fields.html5 import (
    EmailField,
    URLField
)
from wtforms.validators import (
    Email,
    EqualTo,
    InputRequired,
    Length,
    URL
)
from app import db
from app.models import Template

import os, sys #used for getting file type
from urllib.parse import urlparse

def validate_filetype(form, field):
    template_path = field.data
    ext = os.path.splitext(template_path)[1]
    if ext not in ('.json', '.yml', '.yaml'):
        raise ValidationError('Invalid File Type')

def reject_duplicates(form, field):
    print(field.data)
    if Template.query.filter_by(name=field.data).first():
        raise ValidationError('Template name already exists')
    elif Template.query.filter_by(url=field.data).first():
        raise ValidationError('Template url already exists')

class TemplateForm(FlaskForm):
    template_name = StringField('Template Name', validators=[InputRequired(), reject_duplicates])
    template_url = URLField( 'Template URL', validators=[InputRequired(), URL(message='error'), reject_duplicates, validate_filetype])
    submit = SubmitField('Add Template')


        