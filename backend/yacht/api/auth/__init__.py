from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_module(app, **kwargs):
    from .views import blueprint

    jwt.init_app(app)

    app.register_blueprint(blueprint, **kwargs)
