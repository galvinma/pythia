from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import Form
from wtforms.fields import BooleanField, StringField, SubmitField
from wtforms.validators import Required
from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import	declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_login import LoginManager, UserMixin, login_user, login_required


DeclarativeBase = declarative_base()

class User(DeclarativeBase, UserMixin):
	__tablename__ = 'User'

	id = Column('id', Integer, Sequence('user_id'), primary_key=True)
	username = Column('username', String, unique=True)
	firstname = Column('firstname', String)
	lastname = Column('lastname', String)
	email = Column('email', String)
	password = Column('password', String)
	description = Column('description', String)
	profilepicture = Column('profilepicture', String)

	### Relationships ###
	message = relationship("Message", backref = "User")
	user_conversations = relationship("UserConversations", backref ="User" )
	interests = relationship("UserInterests", backref = "User")


class Message(DeclarativeBase):
	__tablename__ = "Message"

	id = Column('id', Integer, Sequence('message_id'), primary_key=True)
	user_id = Column(Integer, ForeignKey('User.id'))
	conversations_id = Column(Integer, ForeignKey('Conversations.id'))
	message = Column('message', String)
	timestamp = Column('timestamp', String)


class UserConversations(DeclarativeBase):
	__tablename__ = "UserConversations"

	user_id = Column(Integer, ForeignKey('User.id'), primary_key=True)
	conversations_id = Column(Integer, ForeignKey('Conversations.id'), primary_key=True)

class Conversations(DeclarativeBase):
	__tablename__ = "Conversations"

	id = Column('id', Integer, Sequence('conversations_id'), primary_key=True)
	timestamp = Column('timestamp', String)

	### Relationships ###
	message = relationship("Message", backref = "Conversations")
	user_conversations = relationship("UserConversations", backref ="Conversations" )


class Interests(DeclarativeBase):
	__tablename__ = "Interests"

	id = Column('id', Integer, Sequence('interests_id'), primary_key=True)
	interest = Column('interest', String)

	### Relationships ###
	user_interests = relationship("UserInterests", backref = "Interests")

class UserInterests(DeclarativeBase):
	__tablename__ = "UserInterests"

	user_id = Column(Integer, ForeignKey('User.id'), primary_key=True)
	interest = Column(Integer, ForeignKey('Interests.id'), primary_key=True)
