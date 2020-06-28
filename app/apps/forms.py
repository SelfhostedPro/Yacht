from flask_wtf import FlaskForm
from wtforms import Form as NoCsrfForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (
    FormField,
    FieldList,
    HiddenField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
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
    NumberRange,
    Optional,
    Regexp,
    URL,
    ValidationError
)
from app import db
from app.models import Template, Compose

import os
import sys  # used for getting file type
from urllib.parse import urlparse
import urllib.request
import docker


# def validate_ports(self, field):
#     dclient = docker.from_env()
#     for app in dclient.containers.list(all=True):
#         for _host_port in app.ports.keys():
#             if host_port == _host_port:
#                 raise ValidationError('port already exists')

class _PortForm(NoCsrfForm):
    cport = IntegerField('Container Port',
        description='The port exposed by the container.',
        validators=[
            Optional(),
            NumberRange(0, 65535)
        ],
        render_kw={
            'placeholder': 'Container Port',
            'aria-discribedby': 'Container Port',
        }
    )
    hport = IntegerField('Host Port',
        description='The port exposed by the host.',
        validators=[
            NumberRange(0, 65535)
        ],
        render_kw={
            'placeholder': 'Host Port',
            'aria-discribedby': 'Host Port',
        }
    )
    proto = SelectField('Protocol',
        description='The protocol used by the connection.',
        choices=[('tcp', 'TCP'), ('udp', 'UDP')],
        validators=[
        ],
        render_kw={
            'aria-discribedby': 'Protocol',
        }
    )

    # TODO:
    # - Check for duplicate host port assignment here!
    # - Check for duplicate container port assignment here!


class _VolumeForm(NoCsrfForm):
    container = StringField(
        'Container Path',
        validators=[
#            InputRequired()
        ]
    )
    bind = StringField(
        'Host Path',
        validators=[
#            InputRequired()
        ]
    )

class _EnvForm(NoCsrfForm):
    # HiddenField!?
    default = HiddenField('Default')
    label = StringField('Label',
        validators=[
            InputRequired()
        ]
    )
    name = StringField(
        'Name',
        validators=[
            Optional()
        ],
        filters = [lambda x: x or None]
    )
    # deprecated:
    # set = StringField('Set')


class DeployForm(FlaskForm):
    name = StringField('App Name', validators=[InputRequired()])
    image = StringField('Image', validators=[InputRequired()])
    ports = FieldList(FormField(_PortForm))
    volumes = FieldList(FormField(_VolumeForm))
    env = FieldList(FormField(_EnvForm))
    restart_policy = StringField('Restart Policy')
    submit = SubmitField('Deploy App')

    def validate_name(self, field):
        dclient = docker.from_env()
        if any(app.name == field.data for app in dclient.containers.list(all=True)):
            raise ValidationError('name already exists')
