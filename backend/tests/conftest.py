import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')


import pytest
from yacht import create_app

@pytest.fixture
def app():
    app = create_app('TESTING')
    app.testing = True
    # with app.app_context():
    #     app.init_db()
    #     # Add some database records here!
    yield app

@pytest.fixture
def client(app):
    # app = create_app() # pass environment as parameter
    # app.testing = True # app.config['TESTING'] = True
    # with app.test_client() as client:
    #     # with app.app_context():
    #     #     app.init_db()
    #     #     get_db().executescript(_data_sql)
    #     yield client
    return app.test_client()
