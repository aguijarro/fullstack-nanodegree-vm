"""
Contains functions used for built the static site of app
"""

from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response
#call Blueprint
from . import mod_web

# Show Index site
@mod_web.route('/', methods=['GET'])
def index():
    """
        Function uses to show a static index page from app.
    """
    return render_template('web/index.html')
