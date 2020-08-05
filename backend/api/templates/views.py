from .. import db
from ..models.containers import (
    Template,
    TemplateItem,
    TemplateVariables
)
from ..models.container_schemes import (
    TemplateSchema,
    TemplateItemSchema,
    TemplateVariablesSchema
)
from ..utils import conv_ports2dict, conv_sysctls2dict

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

from datetime import datetime
import json
from sqlalchemy import or_
from sqlalchemy.orm.session import make_transient
from sqlalchemy.exc import IntegrityError
import urllib.request
from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs
from werkzeug.exceptions import MethodNotAllowed, UnprocessableEntity

templates = Blueprint('templates', __name__)

# endpoint: index
#  methods: GET
#   errors: 200 (OK) | 404 (Not Found)
@templates.route('/')
@jwt_required

# @use_kwargs({'per_page': fields.Int(missing=10)}, locations=('query',))
# ...
def index():
    templates = Template.query.order_by(Template.title).all()
    templates_schema = TemplateSchema(many=True)
    data = templates_schema.dump(templates, many=True)
    return jsonify({ 'data': data })

# endpoint: show
#  methods: GET
#   errors: 200 (OK) | 404 (Not Found)
@templates.route('/<int:id>')
@jwt_required

def show(id):
    try:
        template = Template.query.get_or_404(id)
        template_schema = TemplateSchema()
        data = template_schema.dump(template)
        return jsonify({ 'data': data })
    except IntegrityError as err:
        abort(400, { 'error': 'Bad Request' })

# endpoint: create
#  methods: POST
#   errors: 201 (Created) | [200 (OK) | 204 (No Content)] | 400 (Bad Request)
@templates.route('/', methods=['POST'])
@jwt_required
@use_args(TemplateSchema(), location='json')

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
                sysctls = conv_sysctls2dict(entry.get('sysctls', []))

                # Optional use classmethod from_dict
                template_content = TemplateItem(
                    type = int(entry['type']),
                    title = entry['title'],
                    platform = entry['platform'],
                    description = entry.get('description', ''),
                    name = entry.get('name', entry['title'].lower()),
                    logo = entry.get('logo', ''), # default logo here!
                    image = entry.get('image', ''),
                    notes = entry.get('note', ''),
                    categories = entry.get('categories', ''),
                    restart_policy = entry.get('restart_policy'),
                    ports = ports,
                    volumes = entry.get('volumes', []),
                    env = entry.get('env', []),
                    sysctls = sysctls,
                    cap_add = entry.get('cap_add', [])
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
        db.session.rollback()
        pass

    template_schema = TemplateSchema()
    data = template_schema.dump(template)
    return jsonify({ 'data': data })

# endpoint: edit
#  methods: PUT
#   errors: 201 (Created) | [200 (OK) | 204 (No Content)] | 409 (Conflict)
# endpoint: update
#  methods: PATCH
#   errors: ... 400 (Bad Request) | 409 (Conflict) | 415 (Unsupported Media Type)

# endpoint: delete/destroy
#  methods: DELETE (optional: POST)
#   errors: 204 (No Content) | 404 (Not Found)
@templates.route('/<int:id>', methods=['DELETE'])
@jwt_required

# perhaps use webargs for id
def delete(id):
    '''curl --header "Content-Type: application/json" \
    -X "DELETE" \
    http://127.0.0.1:5000/api/templates/2
    '''

    template = Template.query.get_or_404(id)
    db.session.delete(template)
    db.session.commit()
    
    template_schema = TemplateSchema()
    data = template_schema.dump(template)
    return jsonify({ 'data': data})

# ---

@templates.route('/<int:id>/refresh', methods=['POST'])
@jwt_required

def refresh(id):
    '''curl --header "Content-Type: application/json" \
      --request POST \
      http://127.0.0.1:5000/api/templates/1/refresh
    '''
    template = Template.query.get_or_404(id)

    items = []
    try:
        with urllib.request.urlopen(template.url) as fp:
            for entry in json.load(fp):

                ports = conv_ports2dict(entry.get('ports', []))
                sysctls = conv_sysctls2dict(entry.get('sysctls', []))

                item = TemplateItem(
                    type = int(entry['type']),
                    title = entry['title'],
                    platform = entry['platform'],
                    description = entry.get('description', ''),
                    name = entry.get('name', entry['title'].lower()),
                    logo = entry.get('logo', ''), # default logo here!
                    image = entry.get('image', ''),
                    notes = entry.get('note', ''),
                    categories = entry.get('categories', ''),
                    restart_policy = entry.get('restart_policy'),
                    ports = ports,
                    volumes = entry.get('volumes', []),
                    env = entry.get('env', []),
                    sysctls = sysctls,
                    cap_add = entry.get('cap_add', [])
                )
                items.append(item)
    except Exception as exc:
        print('Template update failed. ERR_001', exc)
        raise
    else:
        db.session.delete(template)
        db.session.commit()

        make_transient(template)
        template.updated_at = datetime.utcnow()
        template.items = items

        try:
            db.session.add(template)
            db.session.commit()
            print(f"Template \"{template.title}\" updated successfully.")
        except Exception as exc:
            db.session.rollback()
            print('Template update failed. ERR_002', exc)
            raise

    template_schema = TemplateSchema()
    data = template_schema.dump(template)
    return jsonify({ 'data': data })


@templates.route('/items')
@jwt_required

# @use_kwargs({'per_page': fields.Int(missing=10)}, locations=('query',))
# ...
def itemindex():
    template_items = TemplateItem.query.order_by(TemplateItem.title).all()
    template_items_schema = TemplateItemSchema(many=True)
    data = template_items_schema.dump(template_items, many=True)
    return jsonify({ 'data': data })

# endpoint: show
#  methods: GET
#   errors: 200 (OK) | 404 (Not Found)
@templates.route('/<int:id>/contents')
@jwt_required

def showitems(id):
    try:
        template_item = TemplateItem.query.get_or_404(id)
        template_item_schema = TemplateItemSchema()
        data = template_item_schema.dump(template_item)
        return jsonify({ 'data': data })
    except IntegrityError as err:
        abort(400, { 'error': 'Bad Request' })

@templates.route('/settings/variables')
@jwt_required

def showvars():
    try:
        template_vars = TemplateVariables.query.all()
        template_var_schema = TemplateVariablesSchema(many=True)
        data = template_var_schema.dump(template_vars)
        return jsonify({ 'data': data })
    except IntegrityError as err:
        abort(400, { 'error': 'Bad Request' })

@templates.route('/settings/variables/set', methods=['POST'])
@jwt_required
@use_args(TemplateVariablesSchema(many=True), location='json')

def setvars(args):
    try:
        template_vars = TemplateVariables.query.all()
        variables = []
        t_vars = args

        for entry in t_vars:
            template_variables = TemplateVariables(
                variable=entry.get("variable"),
                replacement=entry.get("replacement")
            )
            variables.append(template_variables)

        TemplateVariables.query.delete()
        db.session.add_all(variables)
        db.session.commit()

        template_var_schema = TemplateVariablesSchema(many=True)
        data = template_var_schema.dump(t_vars)
        return jsonify({'data': data})

    except IntegrityError as err:
        abort(400, { 'error': 'Bad Request' })