"""
Contains models used for the authentication process
"""
from flask import current_app
from .. import db


class User(db.Model):
    """
        Class used to create users
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(64), unique=True, index=True)
    picture = db.Column(db.String(250))

    def __repr__(self):
        return '<User %r>' % self.name
