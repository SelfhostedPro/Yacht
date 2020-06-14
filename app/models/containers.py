from flask import current_app
from .. import db

class Template(db.Model):
    __tablename__ = 'templates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    url = db.Column(db.String(256), unique=True)
    path = db.Column(db.String(256), unique = True)
    
    #def __repr__(self):
     #   return f"('{self.name}', '{self.url}', '{self.path}')"