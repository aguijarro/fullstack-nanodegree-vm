"""
Contains models used for the catalog process
"""
from flask import current_app
from .. import db
from ..mod_auth.models import User
from datetime import datetime


# Define a TypeTask model

class TypeTask(db.Model):
    """
        Class used to create a type_tasks table
    """
    __tablename__ = 'type_tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(User)

    def __repr__(self):
        return self.name

# Define a Task model
class Task(db.Model):
    """
        Class used to create a task table
    """
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    description = db.Column(db.String(200), unique=True, index=True)
    startDate = db.Column(db.DateTime, default=datetime.utcnow)
    endDate = db.Column(db.DateTime, default=datetime.utcnow)
    task_path = db.Column(db.String(255))
    type_task_id = db.Column(db.Integer, db.ForeignKey('type_tasks.id'))
    type_task = db.relationship(TypeTask)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(User)

    def __repr__(self):
        return '<Task %r>' % self.name

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }
