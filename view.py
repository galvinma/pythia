import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import Form
#from wtforms import Form
from wtforms.fields import BooleanField, StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, scoped_session, query
from sqlalchemy.ext.declarative import	declarative_base
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import func, select
from flask_login import LoginManager, UserMixin, login_user, login_required

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

	@app.route('/', methods =['GET', 'POST'])
	def index():
		session = Session()
		signupform = RegistrationForm()
		loginform = LoginForm()

		if signupform.validate_on_submit():
			user = SignUp(firstname = signupform.firstname.data, lastname = signupform.lastname.data, username = signupform.username.data, email = signupform.email.data, password = signupform.password.data)
			session.add(user)
			session.commit()
			flash('you are now logged in')
			session.close()
			return redirect(url_for('profile', signupform=signupform))

		elif loginform.validate_on_submit():
			session = Session()
			user = session.query(SignUp).filter_by(username = loginform.logusername.data)
			login_user(user)
			flash("You are now logged in, congrats G!")
			return redirect(url_for('profile', loginform=loginform))

		flash('oh noes, you broke it')
		session.close()
		return render_template('signup.html', signupform=signupform, loginform=loginform)	

	@app.route('/profile')	
	def profile():
		return render_template('profile.html')

	@app.route('/search')
	def search():
		return render_template('search.html')

	@app.route('/search_people', methods=['GET', 'POST'])
	def search_people():
		session = Session()
		last = session.query(SignUp).first()
		form = RegistrationForm(obj=last)
		session.close()
		return render_template('search_people.html', form=form)	

	return app

create_app(app)

if __name__ == '__main__':
	app.run()


