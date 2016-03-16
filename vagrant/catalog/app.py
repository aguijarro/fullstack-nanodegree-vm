"""
Based on: Flask Web Development - Miguel Bringer and Udacity https://github.com/udacity/ud330
"""

"""
Contains functions to execute the app
"""
import os

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app, db
#from app.models import User, Follow, Role, Permission, Post, Comment
from flask.ext.script import Manager, Server, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

migrate = Migrate(app, db)
server = Server(host="0.0.0.0", port=8000)

manager = Manager(app)
manager.add_command("runserver", server)

'''
Registers the application and database instances and the models so that they are automatically imported into the shell
'''
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade, migrate
    # migrate database to latest revision
    migrate()
    upgrade()


if __name__ == '__main__':
    manager.run()
