from flask import Blueprint

mod_web = Blueprint('mod_web', __name__,template_folder='templates', static_folder='static')

from . import views, errors
#from ..models import Permission

#@main.app_context_processor
#def inject_permissions():
#    return dict(Permission=Permission)
