from flask import current_app
from .. import db
from datetime import datetime

class Template(db.Model):
    __tablename__ = 'templates'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    url = db.Column(db.String(256), unique=True)
    created_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    items = db.relationship('TemplateContent', backref='template', cascade="save-update, merge, delete, delete-orphan", lazy='dynamic') ### Makes sure template contents are deleted if a template is

    #def __repr__(self):
     #   return f"('{self.name}', '{self.url}', '{self.path}')"

class TemplateContent(db.Model):
    __tablename__ = 'template_content'
    id = db.Column(db.Integer, primary_key=True)
    # type = db.Column(db.String(1))
    type = db.Column(db.Integer)
    title = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64), index=True)
    notes = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    logo = db.Column(db.String)
    image = db.Column(db.String(64))
    categories = db.Column(db.JSON)
    platform = db.Column(db.String(20))
    restart_policy = db.Column(db.String(20))
    sysctls = db.Column(db.JSON, nullable=True)
    ports = db.Column(db.JSON, nullable=True)
    volumes = db.Column(db.JSON, nullable=True)
    env = db.Column(db.JSON, nullable=True)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id')) #Links template content to template above

### Not in use yet
class Compose(db.Model):
    __tablename__ = 'compose'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(256))
    url = db.Column(db.String(256), unique=True)
    path = db.Column(db.String(256), unique = True)
