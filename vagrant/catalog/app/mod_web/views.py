from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response
#call Blueprint
from . import mod_web

# Show Index site
@mod_web.route('/', methods=['GET'])
def index():
    return render_template('web/index.html')
