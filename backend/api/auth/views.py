from ..models.user import User
from ..models.tokens import TokenBlacklist
from .. import db
from .helpers import (
    is_token_revoked, add_token_to_database, get_user_tokens,
    revoke_token, unrevoke_token,
    prune_database
)
from flask import Blueprint
from flask import (
    abort,
    jsonify,
    current_app,
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
import datetime
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

@auth.before_app_first_request
def setup_sqlalchemy():
    db.create_all()

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
    user = User.query.filter_by(username=username).first()
    
    if user is not None and user.verify_password(password):
        refresh_token_expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username, expires_delta=refresh_token_expires)

        add_token_to_database(access_token, current_app.config['JWT_IDENTITY_CLAIM'])
        add_token_to_database(refresh_token, current_app.config['JWT_IDENTITY_CLAIM'])
        data = {
            'username': username,
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return jsonify(data), 200
    return abort(401)

@auth.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    '''curl -H "Authorization: Bearer $REFRESH" -X POST http://127.0.0.1:5000/api/refresh'''
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    add_token_to_database(access_token, current_app.config['JWT_IDENTITY_CLAIM'])
    data = { 'access_token': access_token }
    return jsonify(data), 200

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
    if current_user: return jsonify(identity=current_user), 200
    return jsonify(identity='anonymous'), 200

@auth.route('/token', methods=['GET'])
@jwt_required
def get_tokens():
    user_identity = get_jwt_identity()
    all_tokens = get_user_tokens(user_identity)
    data = [token.to_dict() for token in all_tokens]
    return jsonify(data), 200    

@auth.route('/auth/token/<token_id>', methods=['PUT'])
@jwt_required
def modify_token(token_id):
    # Get and verify the desired revoked status from the body
    json_data = request.get_json(silent=True)
    print(json_data)
    if not json_data:
        return jsonify({"msg": "Missing 'revoke' in body"}), 400
    revoke = json_data.get('revoke', None)
    if revoke is None:
        return jsonify({"msg": "Missing 'revoke' in body"}), 400
    if not isinstance(revoke, bool):
        return jsonify({"msg": "'revoke' must be a boolean"}), 400

    # Revoke or unrevoke the token based on what was passed to this function
    user_identity = get_jwt_identity()
    try:
        if revoke:
            revoke_token(token_id, user_identity)
            return jsonify({'msg': 'Token revoked'}), 200
        else:
            unrevoke_token(token_id, user_identity)
            return jsonify({'msg': 'Token unrevoked'}), 200
    except TokenNotFound:
        return jsonify({'msg': 'The specified token was not found'}), 404

@auth.route('/count')
@jwt_optional
def user_count():
    count = len(User.query.all())
    print(count)
    return jsonify(count), 200