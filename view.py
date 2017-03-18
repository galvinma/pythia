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
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user



from form import RegistrationForm, PeopleSearchForm, LoginForm, MessageForm
from model import DeclarativeBase
from model import SignUp, Message, Messagetotal


app = Flask(__name__)
"app.config.from_object(os.environ['APP_SETTINGS'])"
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

		if loginform.validate_on_submit():
			username = session.query(SignUp).filter_by(username = loginform.logusername.data).first()
			if username and username.password == loginform.logpassword.data:
				login_user(username)
				session.close()
				return render_template('profile.html', loginform=loginform)
			else:
				flash('Username or Password Incorrect')
		session.close()
		return render_template('index.html', loginform=loginform)	

	@app.route('/signup', methods =['GET', 'POST'])
	def signup():
		session = Session()
		signupform = RegistrationForm()
		loginform = LoginForm()

		if signupform.validate_on_submit():
			user = SignUp(firstname = signupform.firstname.data, lastname = signupform.lastname.data, username = signupform.username.data, email = signupform.email.data, password = signupform.password.data)
			session.add(user)
			session.commit()
			username = session.query(SignUp).filter_by(username = signupform.username.data).first()
			login_user(username)
			session.close()
			return redirect(url_for('profile', signupform=signupform))

		elif loginform.validate_on_submit():
			username = session.query(SignUp).filter_by(username = loginform.logusername.data).first()
			if username and username.password == loginform.logpassword.data:
				login_user(username)
				return redirect(url_for('profile', loginform=loginform))
			else:
				flash('Username or Password Incorrect')
		session.close()
		return render_template('signup.html', signupform=signupform, loginform=loginform)	

	@app.route('/profile', methods =['GET', 'POST'])	
	@login_required
	def profile():
		return render_template('profile.html')

	@app.route('/message', methods =['GET', 'POST'])
	@login_required
	def message():
		session = Session()
		messageform = MessageForm()
		user = current_user.username
		if messageform.validate_on_submit():
			message_context = messageform.msgusername.data + ":" + user
			# Spit decision tree based upon if an entry exists in increment table
			# If conversation DNE, create a new traker for number of messages
			if message_context != session.query(Messagetotal).filter(Messagetotal.identity):
				table_construct = Messagetotal(identity = message_context, messagetotal = 0)
				session.add(table_construct)
				session.commit()
				# Increment the number of messages between users
				for var in session.query(Messagetotal).\
					filter(Messagetotal.identity==message_context):
					var.messagetotal = var.messagetotal + 1
					messagesum = str(var.messagetotal)
					session.commit()
					# Add message 
					table_entry_id = str(message_context + ":" + messagesum)
					mes = Message(mes_identity = table_entry_id, message = messageform.message.data, from_user = user)
					session.add(mes)
					session.commit()
					session.close()
			else:	
			# For conversations that exist in increment table
				for var in session.query(Messagetotal).\
						filter(Messagetotal.identity==message_context):
						var.messagetotal = var.messagetotal + 1
						messagesum = str(var.messagetotal)
						session.commit()
						# Add message 
						table_entry_id = str(message_context + ":" + messagesum)
						print table_entry_id
						mes = Message(mes_identity = table_entry_id, message = messageform.message.data, from_user = user)
						session.add(mes)
						session.commit()
						session.close()
		return render_template('message.html', messageform=messageform)


# old code that fails when identity already exists
#
#			if 	message_context == messageform.msgusername.data + ":" + user: # ex. admin:galvinma where galvinma is current user
#				table_construct = Messagetotal(identity = message_context, messagetotal = 0)
#				session.add(table_construct)
#				session.commit()
#				# Increment the number of messages between users
#				for var in session.query(Messagetotal).\
#						filter(Messagetotal.identity==message_context):
#						var.messagetotal = var.messagetotal + 1
#						messagesum = str(var.messagetotal)
#						session.commit()
#						# Add message 
#						table_entry_id = str(message_context + ":" + messagesum)
#						mes = Message(mes_identity = table_entry_id, message = messageform.message.data, from_user = user)
#						session.add(mes)
#						session.commit()
#						session.close()
#		return render_template('message.html', messageform=messageform)


	@app.route('/chat', methods =['GET', 'POST'])
	@login_required
	def chat():
		return render_template('chat.html')	

	@app.route('/search')
	@login_required
	def search():
		return render_template('search.html')

	@app.route('/search_people-', methods=['GET', 'POST'])
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


