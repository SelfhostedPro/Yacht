from .. import db
from ..models.containers import (
    Template,
    TemplateContent
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

import time
import wget
import os  # used for getting file type and deleting files
from urllib.parse import urlparse  # used for getting filetype from url
import urllib.request
import json  # Used for getting template data
import docker

from datetime import datetime
from sqlalchemy.orm.session import make_transient
from sqlalchemy.exc import IntegrityError
from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs
from werkzeug.exceptions import MethodNotAllowed, UnprocessableEntity


templates = Blueprint('templates', __name__)

# endpoint: index
#  methods: GET
#   errors: 200 (OK) | 404 (Not Found)
@templates.route('/')
# @use_kwargs({'per_page': fields.Int(missing=10)}, locations=('query',))
# ...
def index():
    templates = Template.query.all()
    templates_schema = TemplateSchema(many=True)
    data = templates_schema.dump(templates, many=True)
    return jsonify({ 'data': data })

@templates.route('/<int:id>')
@jwt_required
def show(id):
    """ View Template Info """
    try:
        template = Template.query.get(id)
        if not template:
            abort(404, { 'error': 'Not Found' })
        template_schema = TemplateSchema()
        data = template_schema.dump(template)
        return jsonify({ 'data': data })
    except IntegrityError as err:
        abort(400, { 'error': 'Bad Request' })

@templates.route('/', methods=['POST'])
@use_args(TemplateSchema(), location='json')
@jwt_required

def create(args):
    """ Add a new Template """
    '''curl --header "Content-Type: application/json" \
      --request POST \
      --data '{"title":"First Template","url":"https://host.local/template.json"}' \
      http://127.0.0.1:5000/api/templates/
    '''
    template = Template(**args)

    try:
    # Opens the JSON and iterate over the content.
        with urllib.request.urlopen(template.url) as file:
            for entry in json.load(file):

                ports = conv_ports2dict(entry.get('ports', []))

                # Optional use classmethod from_dict
                template_content = TemplateContent(
                    type=int(entry['type']),
                    title=entry['title'],
                    platform=entry['platform'],
                    description=entry.get('description', ''),
                    name=entry.get('name', entry['title'].lower()),
                    logo=entry.get('logo', ''),
                    image=entry.get('image', ''),
                    notes=entry.get('note', ''),
                    categories=entry.get('categories', ''), # default: '' or []
                    restart_policy=entry.get('restart_policy'),
                    sysctls=entry.get('sysctls'),
                    ports=ports,
                    volumes=entry.get('volumes'),
                    env=entry.get('env'),
                )
                template.items.append(template_content)
    except (OSError, TypeError, ValueError) as err:
        # Optional handle KeyError here too.
        print('data request failed', err)
        raise

    try:
        db.session.add(template)
        db.session.commit()
    except IntegrityError as err:
        # TODO raises IntegrityError on duplicates (uniqueness)
        #       status
        pass

    template_schema = TemplateSchema()
    data = template_schema.dump(template)
    return jsonify({ 'data': data })

import re

REGEXP_PORT_ASSIGN = r'^(?:\d{1,5}\:)?\d{1,5}|\:\d{1,5}/(?:tcp|udp)$'

# Input Format:
# [
#     '80:8080/tcp',
#     '123:123/udp'
#     '4040/tcp',
# ]
# Result Format:
# [
#     {
#         'cport': '80',
#         'hport': '8080',
#         'proto': 'tcp',
#     },
#     ...
# ]
def conv_ports2dict(data):
    if not all(isinstance(x, str) for x in data):
        raise TypeError('Expected list or str types.')
    if not all(re.match(REGEXP_PORT_ASSIGN, x, flags=re.IGNORECASE) for x in data):
        raise ValueError('Malformed port assignment.')

    delim = ':'
    portlst = []
    for port_data in data:
        hport, cport = None,port_data
        if delim in cport:
            hport,cport = cport.split(delim, 1)
            if not hport: hport = None
        cport,proto = cport.split('/', 1)
        portlst.append({ 'hport': hport, 'cport': cport, 'proto': proto })
    return portlst

@templates.route('/<int:template_id>/refresh')
def update(template_id):
    template = Template.query.get(template_id)
    if not template:
        abort(404, { 'error': 'Not Found' })
    items = []
    try:
        with urllib.request.urlopen(template.url) as fp:
            for entry in json.load(fp):
                # Optional use classmethod from_dict

                ports = conv_ports2dict(entry.get('ports', []))

                template_content = TemplateContent(
                    type=int(entry['type']),
                    title=entry['title'],
                    platform=entry['platform'],
                    description=entry.get('description', ''),
                    name=entry.get('name', entry['title'].lower()),
                    logo=entry.get('logo', ''),
                    image=entry.get('image', ''),
                    notes=entry.get('note', ''),
                    categories=entry.get('categories', ''), # default: '' or []
                    restart_policy=entry.get('restart_policy'),
                    ports=ports,
                    volumes=entry.get('volumes'),
                    env=entry.get('env'),
                )
                items.append(template_content)
    except Exception as exc:
        # connection problems or incorrect JSON data
        print('Template update failed')
    else:
        oldid = template.id
        db.session.delete(template)
        db.session.commit()

        make_transient(template)
        template.id = None
        template.updated_at = datetime.utcnow()
        template.items = items

        try:
            db.session.add(template)
            db.session.commit()
            print("Template \"" + template.title + "\" updated successfully.")
        except Exception as exc:
            db.session.rollback()
            raise
    assert oldid == template.id, 'id changed on template'
    template_schema = TemplateSchema()
    data = template_schema.dump(template)
    return jsonify({ 'data': data })


@templates.route('/<int:id>', methods=['DELETE'])
@jwt_required

# perhaps use webargs for id
def delete(id):
    """ Delete a Template """
    '''curl --header "Content-Type: application/json" \
    -X "DELETE" \
    http://127.0.0.1:5000/api/templates/2
    '''
    # check error code and return json error
    try:
        template = Template.query.get(id)
        db.session.delete(template)
        db.session.commit()
    except IntegrityError as err:
        abort(400, { 'error': 'Bad Request' })

    template_schema = TemplateSchema()
    data = template_schema.dump(template)
    return jsonify({ 'data': data})
