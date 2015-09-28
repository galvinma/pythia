from app import db
from sqlalchemy.dialects.postgresql import JSON


class Result(db.Model):
    __tablename__ = 'Login'

    first_name = db.Column(db.String, primary_key=True)
    last_name = db.Column(db.String())
    username = db.Column(db.String())
    username_email = db.Column(db.String())
    

    def __init__(self, first_name, last_name, username, username_email):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.username_email = username_email


    def __repr__(self):
        return '<username {}>'.format(self.username)