from app import db
from sqlalchemy import *
from sqlalchemy.engine.url import URL
from sqlalchemy.dialects.postgresql import JSON
from flask_login import UserMixin
from app import login_manager
import settings

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

Login = login()

def db_connect():
    return create_engine(URL(settings.DATABASE))

def create_login_table(engine):
    Login.metadata.create_all(engine)

class user(UserMixin, db.model):
    __tablename = 'users'
    id = db.Column(db.integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    username = db.Column(db.String())
    email = db.Column(db.String())
    password_hash = db.Column(db.string(128))
    role_id = db.Column(db.integer, db.ForeignKey('roles.id'))
    

    def __init__(self, first_name, last_name, username, username_email):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.username_email = username_email


    def __repr__(self):
        return '<username {}>'.format(self.username)
