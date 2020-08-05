
from .. import db

from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash



class Template(db.Model):
    __tablename__ = 'templates'
    id = db.Column(db.Integer, primary_key=True)

    # alternative: DateTime(timezone=True), sqlalchemy.sql.func.now()
    created_at = db.Column(db.DateTime,
        nullable=False, unique=False, index=False,
        default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
        nullable=False, unique=False, index=False,
        default=datetime.utcnow, onupdate=datetime.utcnow)

    # rename to title
    title = db.Column(db.String(255),
        nullable=False, unique=True, index=True)
    url = db.Column(db.Text,
        nullable=False, unique=True, index=False)

    items = db.relationship('TemplateItem',
        backref='template', lazy='dynamic', cascade='all, delete-orphan')

class TemplateItem(db.Model):
    __tablename__ = 'template_item'
    id = db.Column(db.Integer, primary_key=True)

    type= db.Column(db.Integer,
        nullable=False, unique=False, index=False)
    title = db.Column(db.String(255),
        nullable=False, unique=False, index=True)
    platform = db.Column(db.String(64),
        nullable=False, unique=False, index=False)
    description = db.Column(db.Text,
        nullable=True, unique=False, index=False)
    name = db.Column(db.String(255),
        nullable=True, unique=False, index=True)
    logo = db.Column(db.Text,
        nullable=True, unique=False, index=False)
    image = db.Column(db.String(128),
        nullable=True, unique=False, index=False)
    notes = db.Column(db.Text,
        nullable=True, unique=False, index=False)
    categories = db.Column(db.JSON,
        nullable=True, unique=False, index=False)
    restart_policy = db.Column(db.String(20),
        nullable=True, unique=False, index=False)
    ports = db.Column(db.JSON,
        nullable=True, unique=False, index=False)
    volumes = db.Column(db.JSON,
        nullable=True, unique=False, index=False)
    env = db.Column(db.JSON,
        nullable=True, unique=False, index=False)
    sysctls = db.Column(db.JSON,
        nullable=True, unique=False, index=False)
    cap_add = db.Column(db.JSON,
        nullable=True, unique=False, index=False)
    template_id = db.Column(db.Integer,
        db.ForeignKey('templates.id'))

class TemplateVariables(db.Model):
    __tablename__ = 'template_variables'
    id = db.Column(db.Integer, primary_key=True)
    variable = db.Column(db.String(255),
        nullable=False, unique=True, index=True)
    replacement = db.Column(db.String(255),
        nullable=False, unique=True, index=True)