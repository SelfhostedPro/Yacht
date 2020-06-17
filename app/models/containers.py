from flask import current_app
from .. import db

class Template(db.Model):
    __tablename__ = 'templates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    url = db.Column(db.String(256), unique=True)
    items = db.relationship('Template_Content', backref='template', cascade="save-update, merge, delete", lazy='dynamic')
    
    #def __repr__(self):
     #   return f"('{self.name}', '{self.url}', '{self.path}')"

class Template_Content(db.Model):
    __tablename__ = 'template_conent'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(1))
    title = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64), index=True)
    notes = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    logo = db.Column(db.String)
    image = db.Column(db.String(64))
    categories = db.Column(db.JSON)
    platform = db.Column(db.String(20))
    restart_policy = db.Column(db.String(20))
    ports = db.Column(db.JSON, nullable=True)
    volumes = db.Column(db.JSON, nullable=True)
    env = db.Column(db.JSON, nullable=True)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'))


class Compose(db.Model):
    __tablename__ = 'compose'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(256))
    url = db.Column(db.String(256), unique=True)
    path = db.Column(db.String(256), unique = True)