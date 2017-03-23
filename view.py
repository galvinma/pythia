import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import Form
from wtforms.fields import BooleanField, StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, scoped_session, query
from sqlalchemy.ext.declarative import	declarative_base
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import func, select
from sqlalchemy import literal_column, or_
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user



from form import RegistrationForm, LoginForm, MessageForm, ProfileForm
from model import DeclarativeBase
from model import SignUp, Message, Messagetotal, Profile


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
		session = Session()
		profileform = ProfileForm()
		user = current_user.username
		if request.method == 'GET':
			print user
		return render_template('profile.html', profileform=profileform )

	@app.route('/message', methods =['GET', 'POST'])
	@login_required
	def message():
		session = Session()
		messageform = MessageForm()
		user = current_user.username
		timestamp = str(datetime.datetime.now())
		if messageform.validate_on_submit():
			# message_context and alternate_context are used to query the 
			# "Messagetotal" table and increment total message count
			message_context = messageform.msgusername.data + ":" + user
			alternate_context = user + ":" + messageform.msgusername.data
			# Spit decision tree based upon if an entry exists in increment table
			#
			# For conversations that exist in Messagetotal table
			query = session.query(Messagetotal).order_by(Messagetotal.identity)
			for row in query.all():
				if row.identity == message_context:
					print "no increment table update required"
					for var in session.query(Messagetotal).\
						filter(Messagetotal.identity==message_context):
						var.messagetotal = var.messagetotal + 1
						messagesum = str(var.messagetotal)
						session.commit()
						# Add message 
						table_entry_id = str(message_context + ":" + messagesum)
						mes = Message(mes_identity = table_entry_id, message = messageform.message.data, from_user = user, timestamp = timestamp)
						session.add(mes)
						session.commit()
				elif row.identity == alternate_context:
					print "alt: no increment table update required"
					for var in session.query(Messagetotal).\
						filter(Messagetotal.identity==alternate_context):
						var.messagetotal = var.messagetotal + 1
						messagesum = str(var.messagetotal)
						session.commit()
						# Add message 
						table_entry_id = str(alternate_context + ":" + messagesum)
						mes = Message(mes_identity = table_entry_id, message = messageform.message.data, from_user = user, timestamp = timestamp)
						session.add(mes)
						session.commit()	
			# If conversation DNE, create a new row to track the number of messages
			query = session.query(Messagetotal).filter(or_(Messagetotal.identity==message_context, Messagetotal.identity==alternate_context)).first()
			if query is None:
				print "updating the messagetotal table"
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
					mes = Message(mes_identity = table_entry_id, message = messageform.message.data, from_user = user, timestamp = timestamp)
					session.add(mes)
					session.commit()
		messages = []
		# user_query pulls up messages based on a match to the mes_identity column.
		# May need to sort by timestamp in the future
		user_query = session.query(Message).filter(Message.mes_identity.contains(user))
		for match in user_query.all():
			messages.append(match.message)
		session.close()			
		return render_template('message.html', messageform=messageform, user=user, messages=messages)

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


