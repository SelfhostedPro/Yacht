from flask_wtf import FlaskForm
from wtforms import ValidationError, Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
    FieldList,
    FormField
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
from app.models import Template, Compose

import os, sys #used for getting file type
from urllib.parse import urlparse
import urllib.request, json

### Not in use yet
#class _PortForm(Form):
#    port = StringField()
### Not in use yet
class _VolumeForm(Form):
    container = StringField('Container Path')
    bind = StringField('Host Path')
### Not in use yet
class _EnvForm(Form):
    label = StringField('Environment Variable')
    default = StringField('Data', validators=[InputRequired()])
### Form for deploying an application. WIP
class DeployForm(FlaskForm):
    name = StringField('App Name', validators=[InputRequired()])
    image = StringField('Image', validators=[InputRequired()])
    ports = FieldList(StringField('Port'))
    volumes = FieldList(FormField(_VolumeForm))
    env = FieldList(FormField(_EnvForm))
    restart_policy = StringField('Restart Policy', validators=[InputRequired()]) 
    submit = SubmitField('Deploy App')


