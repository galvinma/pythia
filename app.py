import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.engine.url import URL




app = Flask(__name__)
db = SQLAlchemy()
app.config.from_object(os.environ['APP_SETTINGS'])
db.init_app(app)


def create_app(app):

	@app.route('/')
	def index():
		return render_template('index.html')

	@app.route('/signup')
	def sign_up():
		return render_template('signup.html')

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


