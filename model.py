from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy import UniqueConstraint, Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import	declarative_base
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
	profilepicture_filename = Column("profilepicture_filename", String)
    profilepicture_filename_url = Column("profilepicture_filename_url", String)

	# Relationships
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
	lastconvo = Column('lastconvo', String)

	# Relationships
	message = relationship("Message", backref = "Conversations")
	user_conversations = relationship("UserConversations", backref ="Conversations" )


class Interests(DeclarativeBase):
	__tablename__ = "Interests"

	id = Column('id', Integer, Sequence('interests_id'), primary_key=True)
	interest = Column('interest', String)

	# Relationships
	user_interests = relationship("UserInterests", backref = "Interests")

class UserInterests(DeclarativeBase):
	__tablename__ = "UserInterests"

	user_id = Column(Integer, ForeignKey('User.id'), primary_key=True)
	interest_id = Column(Integer, ForeignKey('Interests.id'), primary_key=True)
