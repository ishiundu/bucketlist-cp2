# Resource http://flask-sqlalchemy.pocoo.org/2.1/models/
import passlib
from app import db
from datetime import datetime
from sqlalchemy_utils import PasswordType
# from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):
    """
    This class contains the database schema of the Users
    i.e. Table and Columns"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    password = db.Column(PasswordType(onload=lambda **kwargs: dict(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],
        deprecated=['md5_crypt'],
        **kwargs
    ), ), unique=False, nullable=False)

    def check_password(self, password):
        """Here we verify a user's password"""
        print(self.password, password)
        return self.password == password


class Bucketlists(db.Model):

    __tablename__ = "bucketlists"
    bucketlist_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True)
    description = db.Column(db.String(1000))
    date_created = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow())
    date_modified = db.Column(
        db.DateTime(timezone=True),
        nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                           nullable=False)
    creator = db.relationship('Users',
                              backref=db.backref('bucketlists',
                                                 lazy='dynamic'))

    def __repr___(self):
        return 'Bucket name {} >'.format(self.name)

class Items(db.Model):
    """
    This class contains the database schema of the Items
    i.e. Table and Columns"""

    __tablename__ = "items"

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(1000))
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow())
    date_modified = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow())
    bucketlist_id = db.Column(db.Integer,
                              db.ForeignKey('bucketlists.bucketlist_id'),
                              nullable=False)
    bucketlist = db.relationship('Bucketlists',
                                 backref=db.backref('items', lazy='dynamic'))
