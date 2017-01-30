from config import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
"""Here is where we setup the flask test client and the
SQL Alchemy database session"""


def create_app(config_name):
    """Here we create a flask instance for the application
    and configure it"""
    application = Flask(__name__)

    application.config.from_object(config[config_name])

    db.init_app(application)

    return application


app = create_app('development')
