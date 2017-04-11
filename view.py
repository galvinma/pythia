import os
import time
import datetime
import operator
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import Form
from wtforms.fields import BooleanField, StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, scoped_session, query
from sqlalchemy.ext.declarative import	declarative_base
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import func, select
from sqlalchemy import literal_column, or_
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO
from flask_socketio import send, emit


from form import RegistrationForm, LoginForm, ProfileForm 
from model import DeclarativeBase
from model import User, Message, Conversations, UserConversations, Interests


app = Flask(__name__)
"app.config.from_object(os.environ['APP_SETTINGS'])"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:password@localhost/pythia'
app.secret_key = "6234sdfadfs78dfasd9021dsffds3baf57849sdfssdd057348905fds79340"
socketio = SocketIO(app)



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
		# Get data about current user
		user = current_user.id
		description_query = session.query(User).filter_by(id=user)
		descriptions = []
		# GET request to display user data
		if request.method == 'GET':
			for match in description_query.all():
				descriptions.append(match.description)
			return render_template('profile.html', profileform=profileform, descriptions=descriptions, user=current_user.username)
		# POST request to update user description 
		# Add interests in later story
		if profileform.validate_on_submit():
			profile_info = User(id = user, description = profileform.description.data, profilepicture = profileform.profilepicture.data)
			session.merge(profile_info)
			session.commit()
			session.close()
			for match in description_query.all():
				descriptions.append(match.description)
			return render_template('profile.html', profileform=profileform, descriptions=descriptions, user=current_user.username)
		session.close()
		return render_template('profile.html', profileform=profileform, descriptions=descriptions, user=current_user.username)


	@app.route('/message', methods =['GET', 'POST'])
	@login_required
	def message():
		session = Session()

		session.close()			
		return render_template('message.html')


	@socketio.on('get_conversation')
	def get_conversation():	
		user = current_user.username
		timestamp = str(datetime.datetime.now())

		# Show all conversations for a given user
		conversations = []
		conversation_query = session.query(UserConversations).filter_by(user_id=current_user.id)
		for match in conversation_query.all():
			conversations.append(match.conversations_id)
		convo_user = []
		for convo in conversations:
			other_user_query = 	session.query(UserConversations).\
			join(User, UserConversations.user_id==User.id).\
			add_columns(UserConversations.user_id, UserConversations.conversations_id, User.id, User.username).\
			filter(UserConversations.conversations_id==convo).\
			filter(UserConversations.user_id!=current_user.id)
			for x in other_user_query.all():
				convo_user.append({"user_id":x.username, "conversation_id":convo})
		print convo_user
		emit("userconvo", convo_user, broadcast=True)

	@socketio.on('conversation')
	def show_message(conversation):
		print 'Received message from the client'
		conversation_id = conversation['conversation']
		message_query = session.query(Message).join(User, Message.user_id==User.id).\
					add_columns(Message.id, Message.user_id, Message.conversations_id, Message.message, Message.timestamp, User.id, User.username).\
					filter(Message.conversations_id==conversation_id)
		messages = []
		for match in message_query.all():
			messages.append({'message':match.message, 'user_id':match.username, 'timestamp':match.timestamp})
		emit("newmessage", messages, broadcast = True)

	@socketio.on('message')
	def archive_message(to_user,message):
		# Find id of user sending the message
			from_user = current_user.id
			timestamp = str(datetime.datetime.now())
			print 'from user'
			print from_user
			print message['message']
			# Find id of user recieving the message. In addition to the message, client will need to return both usernames + conversation id.
			foreign_user_list = []
			to_user_query = session.query(User).filter_by(username= to_user['to_user'])
			for match in to_user_query.all():
				foreign_user_list.append(match.id)
			print 'to user'
			foreign_user = foreign_user_list[0]
			print foreign_user
			# Find conversations the current user is a part of
			conversation_id = []
			conversation_id_query = session.query(UserConversations).filter_by(user_id=from_user)
			for match in conversation_id_query.all():
				conversation_id.append(match.conversations_id)
			print 'convesations current user is a part of'
			print conversation_id
			# Find conversations shared by both users
			final_convo = []
			for convo in conversation_id:
				match = session.query(UserConversations).filter(UserConversations.user_id==foreign_user, UserConversations.conversations_id==convo)
				for x in match:
					final_convo.append(x.conversations_id)
			print "matching conversation between current and foreign user"
			print final_convo
			# Create conversation id if one does not exist, then add message
			# Split because finalconvo changes
			if not final_convo:
				convo = Conversations(timestamp = timestamp)
				session.add(convo)
				session.commit()
				session.flush()
				user_convo_1 = UserConversations(user_id = from_user, conversations_id = convo.id)
				session.add(user_convo_1)
				session.commit()
				user_convo_2 = UserConversations(user_id = foreign_user, conversations_id = convo.id)
				session.add(user_convo_2)
				session.commit()
				session.flush()
				message = Message(user_id=from_user, conversations_id=convo.id, message=message['message'], timestamp=timestamp)
				session.add(message)
				session.commit()
				session.flush()
				session.close()
				emit("newconvo", broadcast = True)
			# Add message to db
			else:	
				message = Message(user_id=from_user, conversations_id=final_convo[0], message=message['message'], timestamp=timestamp)
				session.add(message)
				session.commit()
				session.flush()
				session.close()
				messages = []
				message_query = session.query(Message).join(User, Message.user_id==User.id).\
					add_columns(Message.id, Message.user_id, Message.conversations_id, Message.message, Message.timestamp, User.id, User.username).\
					filter(Message.conversations_id==final_convo[0])
				for match in message_query.all():
					messages.append({'message':match.message, 'user_id':match.username, 'timestamp':match.timestamp})
				emit("newmessage", messages, broadcast = True)
	@app.route('/search')
	@login_required
	def search():
		return render_template('search.html')


	@app.route('/logout', methods=['GET', 'POST'])
	def logout():
		logout_user()
		return redirect(url_for('index'))		
	
	return app

create_app(app)

if __name__ == '__main__':
	socketio.run(app, debug=True)


