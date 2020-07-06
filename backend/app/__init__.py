import os, sys

from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


from config import config as Config

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
jwt = JWTManager()


def create_app(config):
    app = Flask(__name__)
    config_name = config

    if not isinstance(config, str):
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app.config.from_object(Config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # not using sqlalchemy event system, hence disabling it

    Config[config_name].init_app(app)

    # Set up extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Configure SSL if platform supports it
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        SSLify(app)

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .templates import templates as templates_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/api')
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
    app.register_blueprint(templates_blueprint, url_prefix='/api/templates')

    return app

def register_endpoints(app):
    @app.route('/')
    def index():
        return '<center><a href="http://127.0.0.1:8080/">Vue-Yacht</a></center><iframe src="http://127.0.0.1:8080/" style="display: block; background: #000; border: none; height: 100vh; width: 100vw;"></iframe>'