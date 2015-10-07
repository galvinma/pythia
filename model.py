from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import Form
from wtforms.fields import BooleanField, StringField, SubmitField
from wtforms.validators import Required
from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import	declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, scoped_session
#

DeclarativeBase = declarative_base()


class SignUp(DeclarativeBase):
	__tablename__ = 'SignUp'

#	id = Column(Integer, primary_key=True)
	username = Column('username', String, primary_key=True)
	firstname = Column('firstname', String)
	lastname = Column('lastname', String)
	email = Column('email', String)
	password = Column('password', String)

	def __init__(self,username,firstname,lastname,email,password):
		self.username = username
		self.firstname = firstname
		self.lastname = lastname
		self.email = email
		self.password = password

