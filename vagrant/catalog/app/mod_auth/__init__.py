"""
Initialize the module
"""
from flask import Blueprint

mod_auth = Blueprint('mod_auth', __name__,template_folder='templates', static_folder='static')

##validar ocmo se maneja los errores por modulo
from . import views, models, helpers
