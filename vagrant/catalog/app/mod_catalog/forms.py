from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class TaskForm(Form):
    name = StringField('What is your task?', validators=[Required()])
    submit = SubmitField('Submit')
