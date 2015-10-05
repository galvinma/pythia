from app import db
from sqlalchemy import *
from sqlalchemy.engine.url import URL
from sqlalchemy.dialects.postgresql import JSON
from flask_login import UserMixin

class User(UserMixin):
    __tablename = 'users'
    id = Column('id', INTEGER, primary_key=True)
    first_name = Column('first_name', TEXT)
    last_name = Column('last_name', TEXT)
    username = Column('username', TEXT)
    email = Column('email', TEXT)
    password_hash = Column('password_hash', INTEGER)
    

    def __init__(self, first_name, last_name, username, email, password_hash):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return self.id

    @classmethod
    def get(self_class, id):
        '''Return user instance of id, return None if not exist'''
        return(id)