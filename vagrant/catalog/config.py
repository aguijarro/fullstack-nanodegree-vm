"""
Define configuration parameters for the app
"""

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for signing cookies
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2
    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED     = True
    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = "secret"
    # Define the number of tasks per pages
    TASK_PER_PAGE = 5

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'postgresql://vagrant:vagrant@localhost/catalog_dev'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    UPLOAD_FOLDER = os.environ.get('DEV_UPLOAD_FOLDER') or os.path.realpath('.') + '/app/static/uploads'

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
