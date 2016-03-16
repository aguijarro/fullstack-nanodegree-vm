"""
Contains forms used for the catalog process
"""
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, FileField, DateField
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required

from .models import TypeTask


class TaskForm(Form):
    """
        Class used to create a task
    """
    typeTask = QuerySelectField('What is your Type Task?', validators=[Required()], get_label='name')
    name = StringField('What is your task?', validators=[Required()])
    description = StringField('Description')
    startDate = DateField('DatePicker', format='%Y-%m-%d')
    endDate = DateField('DatePicker', format='%Y-%m-%d')
    fileTask = FileField('File task', validators=[Required()])
    submit = SubmitField('Submit')

class TypeTaskForm(Form):
    """
        Class used to create a type_task
    """
    name = StringField('What is your type task?', validators=[Required()])
    submit = SubmitField('Submit')
