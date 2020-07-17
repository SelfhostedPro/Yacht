from .. import db
from ..models.containers import (
    Template,
    TemplateItem
)
from ..models.container_schemes import (
    TemplateItemSchema,
    DeploySchema
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

from webargs import fields, validate
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from webargs.flaskparser import use_args, use_kwargs
from werkzeug.exceptions import MethodNotAllowed, UnprocessableEntity

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

@apps.route('/<int:id>')
def list_apps(id):
    try:
        template_item = TemplateItem.query.get_or_404(id)
        template_item_schema = TemplateItemSchema()
        data = template_item_schema.dump(template_item)
        return jsonify({ 'data': data })
    except IntegrityError as err:
        abort(400)


@apps.route('/<int:id>/deploy', methods=['POST'])
@use_args(DeploySchema(), location='json')
def deploy(args, id):
    '''curl -H "Content-Type: application/json" -X POST \
    -d '{"title":"Untitled", "image":"my:image", "ports":[{"proto": "tcp", "hport":2020}]}' \
    http://127.0.0.1:5000/api/apps/1/deploy
    '''
    print(args, id)
    # print(id, title, image)
    # print(args, kwargs)
    return jsonify(data = '')