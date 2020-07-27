from .. import db

from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(64),
        nullable=False, unique=True, index=True)
    password_digest = db.Column(db.String(255),
        nullable=False, unique=False, index=False)

    @property
    def password(self):
        raise AttrinuteError('writeonly attr: password')

    @password.setter
    def password(self, value):
        self.password_digest = generate_password_hash(value)

    def verify_password(self, value):
        return check_password_hash(self.password_digest, value)