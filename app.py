import flask_login 
import os
import settings
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.engine.url import URL
from flask_wtf import Form
from wtforms import validators, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Email, Length, Required
from flask_login import LoginManager
from config import Config
from model import User
from signup import SignupForm


app = Flask(__name__)
db = SQLAlchemy()
app.config.from_object(os.environ['APP_SETTINGS'])
db.init_app(app)

def db_connect():
    return create_engine(URL(settings.DATABASE))


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'



def create_app(app):

	@login_manager.user_loader
	def load_user(id):
		return User.get(id)

	login_manager.setup_app(app)

	@app.route('/')
	def index():
		return render_template('index.html')

	@app.route('/signup', methods=['GET', 'POST'])
	def sign_up():
		form = SignupForm()
		return render_template('signup.html', email='email')

	@app.route('/about')
	def about():
		return render_template('about.html')

	@app.route('/search')
	def search():
		return render_template('search.html')

	@app.route('/profile')
	def profile():
		return render_template('profile.html')
	

	return app

create_app(app)	



if __name__ == '__main__':
	app.run()


