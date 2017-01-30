# Sources: http://flask.pocoo.org/docs/0.12/config/

import os
# Here we return the os path of our directory
base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """This base class contains configs that are common to
all environments.
    """
    SECRET_KEY = 'myl0Xyl0t0'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(base_dir, 'silicon.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    """This class configures the testing environment
properties
    """
    TESTING = True


class ProductionConfig(Config):
    """This class configures the production environment
properties
    """
    TESTING = True
    DEBUG = False


class DevelopmentConfig(Config):
    """This class contains the Development environment
properties
    """
    DEBUG = True
    TESTING = True


config = {
    'testing': TestingConfig,
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
