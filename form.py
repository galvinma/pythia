from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import Form
from wtforms.fields import BooleanField, StringField, SubmitField, TextField, PasswordField
from wtforms.validators import Required
from flask_login import LoginManager, UserMixin, login_user, login_required

class RegistrationForm(Form):
	username = StringField('Username', validators=[Required()])
	firstname = StringField('What is your first name?', validators=[Required()])
	lastname = StringField('What is your last name?', validators=[Required()])
	email = StringField('Email Address', validators=[Required()])
	password = StringField('Password', validators=[Required()])
	submit = SubmitField('Submit')

class LoginForm(UserMixin, Form):
	username = StringField('Username', validators=[Required()])
	password = StringField('Password', validators=[Required()])
	submit = SubmitField('Submit')

class PeopleSearchForm(Form):
	search = StringField('Search for people who have similar interests', validators=[Required()])
	submit = SubmitField('Submit')
