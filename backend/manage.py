#!/usr/bin/env python
import os
import subprocess

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from api import create_app, db
from config import Config
from api.models.user import User
from api.models.containers import TemplateVariables

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()

    user = User(
        username='admin',
        password='pass'
    )
    db.session.add(user)
    db.session.commit()
    variables = []
    t_vars = [
        {"variable": "!config", "replacement": "~/yacht/AppData/Config"},
        {"variable": "!data", "replacement": "~/yacht/AppData/Data"}, 
        {"variable": "!media", "replacement": "~/yacht/Media/"},
        {"variable": "!downloads", "replacement": "~/yacht/Downloads/"},
        {"variable": "!music", "replacement": "~/yacht/Media/Music"},
        {"variable": "!playlists", "replacement": "~/yacht/Media/Playlists"},
        {"variable": "!podcasts", "replacement": "~/yacht/Media/Podcasts"},
        {"variable": "!books", "replacement": "~/yacht/Media/Books"},
        {"variable": "!comics", "replacement": "~/yacht/Media/Comics"},
        {"variable": "!tv", "replacement": "~/yacht/Media/TV"},
        {"variable": "!movies", "replacement": "~/yacht/Media/Movies"},
        {"variable": "!pictures", "replacement": "~/yacht/Media/Photos"},
        {"variable": "!localtime", "replacement": "/etc/localtime"},
        {"variable": "!logs", "replacement": "~/yacht/AppData/Logs"},
        ]
    for entry in t_vars:
        template_variables = TemplateVariables(
            variable=entry.get("variable"),
            replacement=entry.get("replacement")
        )
        variables.append(template_variables)
    db.session.add_all(variables)
    db.session.commit()

@manager.option(
    '-n',
    '--number-users',
    default=10,
    type=int,
    help='Number of each model type to create',
    dest='number_users')
def add_fake_data(number_users):
    """
    Adds fake data to the database.
    """
    User.generate_fake(count=number_users)


@manager.command
def setup_dev():
    """Runs the set-up needed for local development."""
    setup_general()


@manager.command
def setup_prod():
    """Runs the set-up needed for production."""
    setup_general()


def setup_general():
    """Runs the set-up needed for both local development and production.
       Also sets up first admin user."""
    Role.insert_roles()
    admin_query = Role.query.filter_by(name='Administrator')
    if admin_query.first() is not None:
        if User.query.filter_by(email=Config.ADMIN_EMAIL).first() is None:
            user = User(
                first_name='Admin',
                last_name='Account',
                password=Config.ADMIN_PASSWORD,
                confirmed=True,
                email=Config.ADMIN_EMAIL)
            db.session.add(user)
            db.session.commit()
            print('Added administrator {}'.format(user.full_name()))


@manager.command
def format():
    """Runs the yapf and isort formatters over the project."""
    isort = 'isort -rc *.py app/'
    yapf = 'yapf -r -i *.py app/'

    print('Running {}'.format(isort))
    subprocess.call(isort, shell=True)

    print('Running {}'.format(yapf))
    subprocess.call(yapf, shell=True)


if __name__ == '__main__':
    manager.run()
