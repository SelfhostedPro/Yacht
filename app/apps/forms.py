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


# def validate_ports(self, field):
#     dclient = docker.from_env()
#     for app in dclient.containers.list(all=True):
#         for _host_port in app.ports.keys():
#             if host_port == _host_port: 
#                 raise ValidationError('port already exists')

class _PortForm(Form):
    container = StringField('Container Port')
    host = StringField('Host Port')

class _VolumeForm(Form):
    container = StringField('Container Path')
    bind = StringField('Host Path')
# Not in use yet


class _EnvForm(Form):
    label = StringField()
    name = StringField(label)
    default = StringField('Data', validators=[InputRequired()])
# Form for deploying an application. WIP


class DeployForm(FlaskForm):
    name = StringField('App Name', validators=[InputRequired(), validate_name])
    image = StringField('Image', validators=[InputRequired()])
    ports = FieldList(FormField(_PortForm))
    volumes = FieldList(FormField(_VolumeForm))
    env = FieldList(FormField(_EnvForm))
    restart_policy = StringField(
        'Restart Policy', validators=[InputRequired()])
    submit = SubmitField('Deploy App')
