# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for signing cookies
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # SIGA_MAIL_SUBJECT_PREFIX = '[SIGA]'

    # SIGA_MAIL_SENDER = 'SIGA Admin <siga@example.com>'

    # SIGA_ADMIN = os.environ.get('SIGA_ADMIN')

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

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    #MAIL_SERVER = 'smtp.googlemail.com'
    #MAIL_PORT = 587
    #MAIL_USE_TLS = True
    #MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    #MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'postgresql://vagrant:vagrant@localhost/catalog_dev'

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
