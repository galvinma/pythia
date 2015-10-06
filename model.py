from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import Form
from wtforms.fields import BooleanField, StringField, SubmitField
from wtforms.validators import Required

class RegistrationForm(Form):
	firstname = StringField('What is your first name?', validators=[Required()])
	lastname = StringField('What is your last name?', validators=[Required()])
	username = StringField('Username', validators=[Required()])
	email = StringField('Email Address', validators=[Required()])
	password = StringField('Password', validators=[Required()])
	submit = SubmitField('Submit')