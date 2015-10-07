import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import Form
from wtforms.fields import BooleanField, StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from form import RegistrationForm
from model import SignUp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:password@localhost/pythia'
db = SQLAlchemy(app)


def create_app(app):

	@app.route('/')
	def index():
		return render_template('index.html')

	@app.route('/signup', methods=['GET', 'POST'])
	def sign_up():
		original_engine = create_engine('postgresql://admin:password@localhost/pythia')
		Session = sessionmaker(bind=original_engine)
		session = Session()
		form = RegistrationForm()
		if form.validate_on_submit():
			user = SignUp(firstname = form.firstname.data, lastname = form.lastname.data, username = form.username.data, email = form.email.data, password = form.password.data)
			session.add(user)
			session.commit()
			flash('you are now logged in')
			session.close()
			return redirect(url_for('profile'))
		flash('oh noes, you broke it')
		session.close()
		return render_template('signup.html', form=form)

	@app.route('/search')
	def search():
		return render_template('search.html')

	@app.route('/profile')	
	def profile():
		return render_template('profile.html')
	return app


if __name__ == '__main__':
	app.run()


