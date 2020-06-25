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

import os
import sys  # used for getting file type
from urllib.parse import urlparse
import urllib.request
import docker


def validate_name(self, field):
        dclient = docker.from_env()
        if any(app.name == field.data for app in dclient.containers.list(all=True)):
            raise ValidationError('name already exists')


def validate_ports(form, field):
    hp,cp = [],[]
    dclient = docker.from_env()
    for app in dclient.containers.list(all=True):
        assign = app.ports
        a = tuple(assign.keys())
        hp += a
        cp += [assign[k][0]['HostPort'] for k in a if assign[k]]
    for port in field.data:
        a,b = port.split(':',1)
        if a in cp or b in hp:
            raise ValidationError('port already in use')

class _VolumeForm(Form):
    container = StringField('Container Path')
    bind = StringField('Host Path')
# Not in use yet


class _EnvForm(Form):
    label = StringField('Environment Variable')
    default = StringField('Data', validators=[InputRequired()])
# Form for deploying an application. WIP


class DeployForm(FlaskForm):
    name = StringField('App Name', validators=[InputRequired(), validate_name])
    image = StringField('Image', validators=[InputRequired()])
    ports = FieldList(StringField('Port'))
    volumes = FieldList(FormField(_VolumeForm))
    env = FieldList(FormField(_EnvForm))
    restart_policy = StringField(
        'Restart Policy', validators=[InputRequired()])
    submit = SubmitField('Deploy App')
