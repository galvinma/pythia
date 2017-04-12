from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import Form
from wtforms.fields import BooleanField, StringField, SubmitField, TextField, PasswordField, FieldList
from wtforms.validators import Required
from flask_login import LoginManager, UserMixin, login_user, login_required


class RegistrationForm(Form):
	username = StringField('Username', validators=[Required()])
	firstname = StringField('What is your first name?', validators=[Required()])
	lastname = StringField('What is your last name?', validators=[Required()])
	email = StringField('Email Address', validators=[Required()])
	password = PasswordField('Password', validators=[Required()])
	submit = SubmitField('Submit')

class LoginForm(Form):
	logusername = StringField('Username', validators=[Required()])
	logpassword = PasswordField('Password', validators=[Required()])
	logsubmit = SubmitField('Login')
