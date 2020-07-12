from .. import db
from ..models.containers import (
    Template,
    TemplateItem
)
from ..models.container_schemes import (
    TemplateSchema
)

from flask import Blueprint
from flask import (
    abort,
    jsonify,
    make_response,
    request
)
from flask_jwt_extended import (
    jwt_required,
    jwt_optional
)

import os  # used for getting file type and deleting files
from urllib.parse import urlparse  # used for getting filetype from url
import urllib.request
import json  # Used for getting template data
import docker

apps = Blueprint('apps', __name__)

@apps.route('/')
def index():
    apps_list = []
    dclient = docker.from_env()
    apps = dclient.containers.list(all=True)
    for app in apps:
        apps_list.append(app.attrs)
    data = apps_list
    return jsonify({ 'data': data })