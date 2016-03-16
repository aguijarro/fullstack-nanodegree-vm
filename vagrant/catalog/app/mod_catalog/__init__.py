"""
Initialize the module
"""

from flask import Blueprint

mod_catalog = Blueprint('mod_catalog', __name__,url_prefix='/catalog',template_folder='templates', static_folder='static')


from . import views, forms
