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
from model import User, Message, Conversations, UserConversations, Profile, Interests


app = Flask(__name__)
"app.config.from_object(os.environ['APP_SETTINGS'])"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:password@localhost/pythia'
app.secret_key = "623478902135784905734890579340"



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
		return session.query(User).get(username)


	@app.route('/', methods =['GET', 'POST'])
	def index():
		session = Session()
		signupform = RegistrationForm()
		loginform = LoginForm()

		if loginform.validate_on_submit():
			username = session.query(User).filter_by(username = loginform.logusername.data).first()
			if username and username.password == loginform.logpassword.data:
				login_user(username)
				session.close()
				return redirect(url_for('profile', loginform=loginform))
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
			user = User(firstname = signupform.firstname.data, lastname = signupform.lastname.data, username = signupform.username.data, email = signupform.email.data, password = signupform.password.data)
			session.add(user)
			session.commit()
			username = session.query(User).filter_by(username = signupform.username.data).first()
			login_user(username)
			session.close()
			return redirect(url_for('profile', signupform=signupform))

		elif loginform.validate_on_submit():
			username = session.query(User).filter_by(username = loginform.logusername.data).first()
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
		descriptions = []
		interests = []

		description_query = session.query(Profile).filter(Profile.id.contains(user))
		interest_query = session.query(Interests).filter(Interests.identity.contains(user))
		if request.method == 'GET':
			for match in description_query.all():
				descriptions.append(match.description)
			for match in interest_query.all():
				interests.append(match.interest)
			return render_template('profile.html', profileform=profileform,interests=interests, user = user, descriptions=descriptions)
		if profileform.validate_on_submit():
			profile_info = Profile(identity = user, description = profileform.description.data, profilepicture = user)
			profile_interests = Interests(identity = user, interest = profileform.interests.data)
			session.merge(profile_info)
			session.add(profile_interests)
			session.commit()
			session.close()
			for match in description_query.all():
				descriptions.append(match.description)
			for match in interest_query.all():
				interests.append(match.interest)
			return render_template('profile.html', profileform=profileform,interests=interests, user = user, descriptions=descriptions)
		session.close()
		return render_template('profile.html', profileform=profileform,interests=interests, user = user, descriptions=descriptions)



	@app.route('/message', methods =['GET', 'POST'])
	@login_required
	def message():
		session = Session()
		messageform = MessageForm()
		user = current_user.username
		timestamp = str(datetime.datetime.now())
		if messageform.validate_on_submit():
			# Add Conversation
			conversation_test = Conversations(timestamp=timestamp)
			session.add(conversation_test)
			session.commit()
			# Add User-Conversation
			session.flush()
		#	user_convo = UserConversations(username = User.username, conversation = Conversations.id)
		#	session.add(user_convo)
		#	session.commit()
			# Add message 
#			message = Message(message = messageform.message.data, timestamp = timestamp)
#			session.add(mes)
#			session.commit()
		messages = []
		# user_query pulls up messages based on a match to the mes_identity column.
		# May need to sort by timestamp in the future
#		user_query = session.query(Message).filter(Message.mes_identity.contains(user))
#		for match in user_query.all():
#			messages.append(match.message)
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
		last = session.query(User).first()
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
	app.debug = True
	app.run()


