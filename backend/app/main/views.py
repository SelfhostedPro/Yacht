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


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify({ 'message': 'Hello API.'})

@main.route('/sample')
@jwt_required
def sample():
    return jsonify({ 'message': 'Hello from Flask API.'})