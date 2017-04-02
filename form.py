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
	password = PasswordField('Password', validators=[Required()])
	submit = SubmitField('Submit')

class LoginForm(Form):
	logusername = StringField('Username', validators=[Required()])
	logpassword = PasswordField('Password', validators=[Required()])
	logsubmit = SubmitField('Login')

# Allows user to send a message
class MessageForm(Form):
	msgusername = StringField('Send to:  ', validators=[Required()])
	message = StringField('Message:  ', validators=[Required()])
	messagesubmit = SubmitField('Send Message')


# Allows user to begin a new conversation
class ConversationForm(Form):
	conversationtitle = StringField('Conversation Name: ')
	conversationsubmit = SubmitField('Create Conversation')

# Allows user to submit new profile information and associated interests.
class ProfileForm(Form):
	description = StringField('Description here  ', validators=[Required()])
	interests = StringField('Interests here:  ')
	profilepicture = StringField('Profile picture')
	profilesubmit = SubmitField('Submit')
