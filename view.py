import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import Form
from wtforms.fields import BooleanField, StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, scoped_session, query
from sqlalchemy.ext.declarative import	declarative_base
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import func, select
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

from form import RegistrationForm, PeopleSearchForm, LoginForm
from model import SignUp, DeclarativeBase

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:password@localhost/pythia'
app.secret_key = "secretkey"


def create_app(app):

	original_engine = create_engine('postgresql://admin:password@localhost/pythia')
	Session = sessionmaker(bind=original_engine)
	metadata = DeclarativeBase.metadata
	metadata.create_all(original_engine)
	session = Session()

	login_manager = LoginManager()
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(username):
		return session.query(SignUp).get(username)

	@app.route('/', methods =['GET', 'POST'])
	def index():
		session = Session()
		signupform = RegistrationForm()
		loginform = LoginForm()

		if signupform.validate_on_submit():
			user = SignUp(firstname = signupform.firstname.data, lastname = signupform.lastname.data, username = signupform.username.data, email = signupform.email.data, password = signupform.password.data)
			session.add(user)
			session.commit()
			username = session.query(SignUp).filter_by(username = signupform.username.data).first()
			login_user(username)
			return redirect(url_for('profile', signupform=signupform))

		elif loginform.validate_on_submit():
			username = session.query(SignUp).filter_by(username = loginform.logusername.data).first()
			login_user(username)
			return redirect(url_for('profile', loginform=loginform))

		session.close()
		return render_template('signup.html', signupform=signupform, loginform=loginform)	

	@app.route('/profile')	
	@login_required
	def profile():
		return render_template('profile.html')

	@app.route('/search')
	@login_required
	def search():
		return render_template('search.html')

	@app.route('/search_people', methods=['GET', 'POST'])
	@login_required
	def search_people():
		session = Session()
		last = session.query(SignUp).first()
		form = RegistrationForm(obj=last)
		session.close()
		return render_template('search_people.html', form=form)	


 	@app.route('/logout', methods=['GET', 'POST'])
	def logout():
		logout_user()
		return redirect(url_for('index'))
	
	return app

create_app(app)

if __name__ == '__main__':
	app.run()


