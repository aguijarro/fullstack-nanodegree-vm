from flask import current_app
from .. import db


# Define a TypeTask model

class TypeTask(db.Model):
    __tablename__ = 'type_task'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Type Task %r>' % self.name

# Define a Task model
class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<Task %r>' % self.name
