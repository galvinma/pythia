from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import Form
from wtforms.fields import BooleanField, StringField, SubmitField
from wtforms.validators import Required
from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import	declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_login import LoginManager, UserMixin, login_user, login_required

#

DeclarativeBase = declarative_base()

class SignUp(DeclarativeBase, UserMixin):
	__tablename__ = 'SignUp'

	username = Column('username', String, primary_key=True)
	firstname = Column('firstname', String)
	lastname = Column('lastname', String)
	email = Column('email', String)
	password = Column('password', String)

	def __init__(self, username,firstname,lastname,email,password):
		self.username = username
		self.firstname = firstname
		self.lastname = lastname
		self.email = email
		self.password = password

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.username

	def __unicode__(self):
		return self.username


class Messagetotal(DeclarativeBase):
	__tablename__ = "Messagetotal"

	identity = Column('identity', String, primary_key=True)
	messagetotal = Column('messagetotal', Integer)

	def __init__(self, identity, messagetotal):
		self.identity = identity
		self.messagetotal = messagetotal

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.identity

	def __unicode__(self):
		return self.identity

class Message(DeclarativeBase):
	__tablename__ = "Message"

	mes_identity = Column('mes_identity', String, primary_key=True)
	message = Column('message', String)
	from_user = Column('from_user', String)
	timestamp = Column('timestamp', String)

	def __init__(self, mes_identity, message, from_user,timestamp):
		self.mes_identity = mes_identity
		self.message = message
		self.from_user = from_user
		self.timestamp = timestamp

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.mes_identity

	def __unicode__(self):
		return self.mes_identity


class Profile(DeclarativeBase):
	__tablename__ = "Profile"

	identity = Column('identity', String, primary_key=True)
	description = Column('descrption', String)
	profilepicture = Column('profilepicture', String)

	def __init__(self, identity, description, profilepicture):
		self.identity = identity
		self.description = description
		self.profilepicture = profilepicture


	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.identity

	def __unicode__(self):
		return self.identity


class Interests(DeclarativeBase):
	__tablename__ = "Interests"

	id = Column('id', Integer, Sequence('interest_id'), primary_key=True)
	identity = Column('identity', String)
	interest = Column('interest', String)

	def __init__(self, identity, interest):
		self.identity = identity
		self.interest = interest



	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.identity

	def __unicode__(self):
		return self.identity	