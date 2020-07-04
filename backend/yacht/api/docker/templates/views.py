from .... import db
from ..models import (
    Template
)
from ..schemes import (
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
from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs
from werkzeug.exceptions import MethodNotAllowed, UnprocessableEntity


blueprint = Blueprint(
    'api.docker.templates',
    __name__,
    url_prefix='/api/docker/templates'
)

@blueprint.route('/')
def index():
    templates = Template.query.all()
    templates_schema = TemplateSchema(many=True)
    data = templates_schema.dump(templates, many=True)
    return jsonify({ 'data': data })

@blueprint.route('/', methods=['POST'])
@use_args(TemplateSchema(), location='json')
def create(args):
    '''curl --header "Content-Type: application/json" \
      --request POST \
      --data '{"name":"First Template","url":"https://host.local/template.json"}' \
      http://127.0.0.1:5000/api/templates/
    '''
    template = Template(**args)
    # TODO raises IntegrityError on duplicates (uniqueness)
    db.session.add(template)
    db.session.commit()
    template_schema = TemplateSchema()
    data = template_schema.dump(template)
    return jsonify({ 'data': data })

@blueprint.route('/<int:id>', methods=['DELETE'])
# perhaps use webargs for id 
def delete(id):
    '''curl --header "Content-Type: application/json" \
    -X "DELETE" \
    http://127.0.0.1:5000/api/templates/2
    '''
    template = Template.query.get_or_404(id)
    template_schema = TemplateSchema()
    data = template_schema.dump(template)
    return jsonify({ 'data': data})
