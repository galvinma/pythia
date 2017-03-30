from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import Form
from wtforms.fields import BooleanField, StringField, SubmitField
from wtforms.validators import Required
from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import	declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_login import LoginManager, UserMixin, login_user, login_required


DeclarativeBase = declarative_base()

class User(DeclarativeBase, UserMixin):
	__tablename__ = 'User'

	id = Column('id', Integer, Sequence('User_id'), primary_key=True)
	username = Column('Username', String, unique=True)
	firstname = Column('Firstname', String)
	lastname = Column('Lastname', String)
	email = Column('Email', String)
	password = Column('Password', String)

	message = relationship("Message")
	userconversation = relationship("UserConversations")
	user_c = relationship("User", back_populates = "user_p")

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
		return self.id

	def __unicode__(self):
		return self.id


class Message(DeclarativeBase):
	__tablename__ = "Message"

	id = Column('id', Integer, Sequence('Message_id'), primary_key=True)
	message = Column('Message', String)
	timestamp = Column('Timestamp', String)

	from_user = Column(String, ForeignKey('User.Username'))
	conversation = Column(Integer, ForeignKey('Conversations.id'))

	def __init__(self, message, timestamp, from_user):
		self.message = messages
		self.timestamp = timestamp
		self.from_user = from_user
		self.conversation = conversation

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.id

	def __unicode__(self):
		return self.id


class UserConversations(DeclarativeBase):
	__tablename__ = "UserConversations"

	username = Column(String, ForeignKey('User.Username'), primary_key=True)
	conversation = Column(Integer, ForeignKey('Conversations.id'), primary_key=True)
	conversation_c = relationship("Conversations", back_populates = "conversation_p")
	user_c = relationship("User", back_populates = "user_p")

	def __init__(self, username, conversation):
		self.username = username
		self.conversation = conversation


class Conversations(DeclarativeBase):
	__tablename__ = "Conversations"

	id = Column('id', Integer, Sequence('Conversations_id'), primary_key=True)
	timestamp = Column('Timestamp', String)

	conversation_p = relationship("UserConversations", back_populates = "conversation_c")
	message = relationship("Message")

	def __init__(self, timestamp):
		self.timestamp = timestamp

	def get_id(self):
		return self.id

	def __unicode__(self):
		return self.id



class Profile(DeclarativeBase):
	__tablename__ = "Profile"

	id = Column(String, ForeignKey('User.Username'), primary_key=True)
	description = Column('descrption', String)
	profilepicture = Column('profilepicture', String)

	def __init__(self, description, profilepicture):
		self.description = description
		self.profilepicture = profilepicture


	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.id

	def __unicode__(self):
		return self.id


class Interests(DeclarativeBase):
	__tablename__ = "Interests"

	id = Column('id', Integer, Sequence('Interests_id'), primary_key=True)
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
		return self.id

	def __unicode__(self):
		return self.id	