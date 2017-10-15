from flask_wtf import Form
from wtforms.fields import BooleanField, StringField, SubmitField, TextField, PasswordField
from wtforms.validators import Required
from flask_wtf.file import FileField, FileRequired

class RegistrationForm(Form):
	username = StringField('Username', validators=[Required()])
	firstname = StringField('What is your first name?', validators=[Required()])
	lastname = StringField('What is your last name?', validators=[Required()])
	email = StringField('Email Address', validators=[Required()])
	password = PasswordField('Password', validators=[Required()])
	submit = SubmitField('Submit')

class LoginForm(Form):
	lg_username = StringField('Username', validators=[Required()])
	lg_password = PasswordField('Password', validators=[Required()])
	submit = SubmitField('Login')

class ProfileForm(Form):
	profilepicture = FileField('Profile picture', validators=[FileRequired()])
