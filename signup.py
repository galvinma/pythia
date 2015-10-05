from flask import Flask
from flask_wtf import Form
from wtforms import validators, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Email, Length, Required



class SignupForm(Form):
	email = StringField("Email", validators=[Required(), Length(1,64), Email()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log in')