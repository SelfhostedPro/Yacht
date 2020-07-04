
from ... import db

from datetime import datetime

# https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Template/template.json

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
    name = db.Column(db.String(255),
        nullable=False, unique=True, index=True)
    url = db.Column(db.Text,
        nullable=False, unique=True, index=False)

    # items = db.relationship('TemplateItem',
    #     backref='template', lazy='dynamic', cascade='all, delete-orphan')
