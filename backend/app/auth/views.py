
from flask import Blueprint
from flask import (
    abort,
    jsonify,
    make_response,
    request
)
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    jwt_refresh_token_required,
    jwt_optional
)
from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs
from werkzeug.exceptions import MethodNotAllowed, UnprocessableEntity


auth = Blueprint('auth', __name__)


# @blueprint.route('/')
# def index():
#     return jsonify({ 'message': 'Hello API.'})
#
# @blueprint.route('/sample')
# def sample():
#     return jsonify({ 'message': 'Hello from Flask API.'})


@auth.route('/login', methods=['POST'])
@use_kwargs(
    {
        'username': fields.Str(required=True),
        'password': fields.Str(required=True),
    },
    location='json'
)
def login(username, password):
    '''curl -H "Content-Type: application/json" -X POST \
    -d '{"username":"user", "password":"pass"}' http://127.0.0.1:5000/api/login'''

    if username != 'user' or password != 'pass':
        # TODO Must go shorter!
        abort(401, 'Invalid authentication credentials',
            make_response(jsonify(message='Invalid authentication credentials'), 401))

    acc_token = create_access_token(identity=username, fresh=True)
    ref_token = create_refresh_token(identity=username)

    # TODO Store the tokens to database

    return jsonify({'access_token': acc_token, 'refresh_token': ref_token}), 200

@auth.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    '''curl -H "Authorization: Bearer $REFRESH" -X POST http://127.0.0.1:5000/api/refresh'''

    current_user = get_jwt_identity()
    acc_token = create_access_token(identity=current_user, fresh=False)
    # TODO Store the token to database
    return jsonify({'access_token': acc_token}), 201

@auth.route('/secure')
@jwt_required
def secure():
    '''curl -H "Authorization: Bearer $ACCESS_TOKEN" http://127.0.0.1:5000/api/secure'''
    current_user = get_jwt_identity()
    return jsonify(logged_as=current_user), 200

@auth.route('/secure-opt')
@jwt_optional
def secure_opt():
    '''curl http://127.0.0.1:5000/api/secure-opt'''
    current_user = get_jwt_identity()
    if current_user: return jsonify(logged_as=current_user), 200
    else: return jsonify(logged_as='anonymous'), 200


# errors raised by webargs
#
# @blueprint.errorhandler(MethodNotAllowed)
# def handle_405(e):
#     d = {
#         'code': 405,
#         'message': 'Method Not Allowed',}
#     return make_response(jsonify(d), 405)
#
# @blueprint.errorhandler(UnprocessableEntity)
# def handle_422(e):
#     print(e)
#     d = {
#         'code': 422,
#         'message': 'Unprocessable Entity',}
#     return make_response(jsonify(d), 422)
