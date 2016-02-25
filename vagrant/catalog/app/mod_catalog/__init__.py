from flask import Blueprint

mod_catalog = Blueprint('mod_catalog', __name__,template_folder='templates', static_folder='static')

##validar ocmo se maneja los errores por modulo
from . import views, forms
