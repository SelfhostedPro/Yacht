from app.auth.views import auth # noqa
from flask_jwt_extended import JWTManager
jwt = JWTManager()

def create_module(app, **kwargs):
    from ..errors import register_errorhandlers

    jwt.init_app(app)
    register_errorhandlers(blueprint)