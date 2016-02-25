# Import flask and template operators
from flask import Flask, render_template
# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy
# Import Login
from flask.ext.login import LoginManager
# Import Bootstrap
from flask.ext.bootstrap import Bootstrap
# Configurations
from config import config


# Define the database object which is imported by modules and controllers
db = SQLAlchemy()
# Define the bootstrap object which is imported by templates
bootstrap = Bootstrap()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    #mail.init_app(app)
    #moment.init_app(app)
    db.init_app(app)

    from app.mod_web import mod_web as web_module
    from app.mod_catalog import mod_catalog as catalog_module
    from app.mod_auth import mod_auth as auth_module

    app.register_blueprint(web_module)
    app.register_blueprint(catalog_module)
    app.register_blueprint(auth_module)

    return app
