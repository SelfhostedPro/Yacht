
def create_module(app, **kwargs):
    from .views import blueprint
    app.register_blueprint(blueprint, **kwargs)
