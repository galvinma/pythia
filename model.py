from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import Form
from wtforms.fields import BooleanField, StringField, SubmitField
from wtforms.validators import Required
from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import	declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
#

DeclarativeBase = declarative_base()


class SignUp(DeclarativeBase):
	__tablename__ = "signup"

	id = Column(Integer, primary_key=True)
	firstname = Column('firstname', String)
	lastname = Column('lastname', String)
	username = Column('username', String)
	email = Column('email', String)
	password = Column('password', String)

	def __repr__(self,id):
		return'<id {}>'.format(self.id)

