from .. import db
from ..models.containers import (
    Template
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
from sqlalchemy.exc import IntegrityError
from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs
from werkzeug.exceptions import MethodNotAllowed, UnprocessableEntity


templates = Blueprint('templates', __name__)

@templates.route('/')
# @use_kwargs({'per_page': fields.Int(missing=10)}, locations=('query',))
# ...
def index():
    templates = Template.query.all()
    templates_schema = TemplateSchema(many=True)
    data = templates_schema.dump(templates, many=True)
    return jsonify({ 'data': data })

@templates.route('/<int:id>')
def show(id):
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
def create(args):
    '''curl --header "Content-Type: application/json" \
      --request POST \
      --data '{"title":"First Template","url":"https://host.local/template.json"}' \
      http://127.0.0.1:5000/api/templates/
    '''
    template = Template(**args)
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

@templates.route('/<int:id>', methods=['DELETE'])
# perhaps use webargs for id
def delete(id):
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
