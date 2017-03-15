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


class TotalMessage(DeclarativeBase):
	__tablename__ = "Message"

	identity = Column('identity', String, primary_key=True)
	message = Column('message', String)

	def __init__(self, msgusername, message):
		self.msgusername = msgusername
		self.message = message

class Message(DeclarativeBase):
	__tablename__ = "Message"

	identity = Column('identity', String, primary_key=True)
	message = Column('message', String)

	def __init__(self, msgusername, message):
		self.msgusername = msgusername
		self.message = message