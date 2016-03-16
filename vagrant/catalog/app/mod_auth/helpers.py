"""
Contains functions used for the authentication process
"""
from flask import current_app

from .models import User
from .. import db

def createUser(login_session):
    """
        Function used to create a user
    """
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    db.session.add(newUser)
    db.session.commit()
    user = db.session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """
        Function used to return a user information
    """
    user = db.session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """
        Function used to return a user information
    """     
    try:
        user = db.session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None
