from ..models.user import User
from ..models.tokens import TokenBlacklist
from .. import db
from .helpers import (
    is_token_revoked, add_token_to_database, get_user_tokens,
    revoke_token, prune_database
)
from .exceptions import TokenNotFound
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
    set_access_cookies,
    create_refresh_token,
    set_refresh_cookies,
    unset_jwt_cookies,
    get_jwt_identity,
    jwt_required,
    jwt_refresh_token_required,
    jwt_optional,
    get_raw_jwt
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
# @blueprint.route('/sample')from exceptions import TokenNotFound
#     return jsonify({ 'message': 'Hello from Flask API.'})

# @auth.before_app_first_request
# def setup_sqlalchemy():
#     db.create_all()

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
        access_token_expires = datetime.timedelta(minutes=30)
        access_token = create_access_token(identity=user.username, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(identity=user.username, expires_delta=refresh_token_expires)

        add_token_to_database(access_token, current_app.config['JWT_IDENTITY_CLAIM'])
        add_token_to_database(refresh_token, current_app.config['JWT_IDENTITY_CLAIM'])

        data = jsonify({'username': username,})
        set_access_cookies(data, access_token)
        set_refresh_cookies(data, refresh_token)
        prune_database()
        return data, 200
    return abort(401)

# @auth.route('/register', methods=['POST'])
# @use_kwargs(
#     {
#         'username': fields.Str(required=True),
#         'password': fields.Str(required=True),
#     },
#     location='json'
# )
# def register(username, password):
#     '''curl -H "Content-Type: application/json" -X POST \
#     -d '{"username":"user", "password":"pass"}' http://127.0.0.1:5000/api/register'''
#     if len(User) < 1 and username is not None and password is not None:
#         # Add user to db
#         user = User(
#             username=username,
#             password=password
#         )
#         db.session.add(user)
#         db.session.commit()
        
#         # Give tokens for immediate login
#         refresh_token_expires = datetime.timedelta(days=1)
#         access_token = create_access_token(identity=user.username)
#         refresh_token = create_refresh_token(identity=user.username, expires_delta=refresh_token_expires)

#         add_token_to_database(access_token, current_app.config['JWT_IDENTITY_CLAIM'])
#         add_token_to_database(refresh_token, current_app.config['JWT_IDENTITY_CLAIM'])
#         data = {
#             'username': username,
#             'access_token': access_token,
#             'refresh_token': refresh_token
#         }
#         return jsonify(data), 200
#     return abort(401)

@auth.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    '''curl -H "Authorization: Bearer $REFRESH" -X POST http://127.0.0.1:5000/api/refresh'''
    refresh_token = get_raw_jwt()
    if is_token_revoked(refresh_token):
        print("Token Revoked" + refresh_token)
        return abort(401)
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    add_token_to_database(access_token, current_app.config['JWT_IDENTITY_CLAIM'])

    data = jsonify({ 'refresh': True })
    set_access_cookies(data, access_token)
    return data, 200

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

@auth.route('/logout', methods=['POST'])
@jwt_required
def logout():
    '''curl -H "Authorization: Bearer $REFRESH" -X POST http://127.0.0.1:5000/api/logout'''
    # Revoke refresh token
    user_identity = get_jwt_identity()
    try:
        revoke_token(user_identity)
        data = jsonify({"msg": "Successfully logged out"})
        unset_jwt_cookies(data)
        return data, 200
    except TokenNotFound:
        return jsonify({'msg': 'The specified token was not found'}), 404

@auth.route('/changePassword', methods=['POST'])
@jwt_required
@use_kwargs(
    {
        'username': fields.Str(required=True),
        'newPassword': fields.Str(required=False),
        'oldPassword': fields.Str(required=True)
    },
    location='json'
)

def changePassword(username, newPassword, oldPassword):
    '''curl -H "Content-Type: application/json" -X POST \
    -d '{"username":"user", "password":"pass"}' http://127.0.0.1:5000/api/login'''
    token = get_raw_jwt()
    jwt_user = get_jwt_identity()
    
    user = User.query.filter_by(username=jwt_user).first()
    
    if user is not None and user.verify_password(oldPassword) and not is_token_revoked(token):
        user.username = username
        user.password = newPassword
        revoke_token(jwt_user)
        
        refresh_token_expires = datetime.timedelta(days=1)
        access_token_expires = datetime.timedelta(minutes=5)
        access_token = create_access_token(identity=user.username, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(identity=user.username, expires_delta=refresh_token_expires)

        add_token_to_database(access_token, current_app.config['JWT_IDENTITY_CLAIM'])
        add_token_to_database(refresh_token, current_app.config['JWT_IDENTITY_CLAIM'])
        
        db.session.add(user)
        db.session.commit()
        
        data = {
            'username': username,
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return jsonify(data), 200
    return abort(401)