from flask_testing import TestCase
from run import app


class GlobalTestCase(TestCase):
    """This class holds the Global Test Case that creates the testing app"""

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            "sqlite:///Test.db"
        app.config['TESTING'] = True
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        return app
