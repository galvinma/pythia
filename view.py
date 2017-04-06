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
from flask_socketio import SocketIO
from flask_socketio import send, emit


from form import RegistrationForm, LoginForm, MessageForm, ProfileForm, ConversationForm
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
		messageform = MessageForm()
		user = current_user.username
		conversationform = ConversationForm()
		timestamp = str(datetime.datetime.now())
		if conversationform.validate_on_submit() and conversationform.conversationsubmit.data:
			# Add Conversation
			conversation = Conversations(timestamp=timestamp)
			session.add(conversation)
			session.commit()
			# Add UserConversation
			session.flush()
			userconversation = UserConversations(user_id=current_user.id, conversations_id=conversation.id)
			session.add(userconversation)
			session.commit()
		if messageform.validate_on_submit() and messageform.messagesubmit.data:
			# Add message
			session.flush() 
			message = Message(user_id=current_user.id, conversations_id=conversation.id, message=messageform.message.data, timestamp=timestamp)
			session.add(message)
			session.commit()
		# Show all conversations for a given user
		conversations = []
		conversation_query = session.query(UserConversations).filter_by(user_id=current_user.id)
		for match in conversation_query.all():
			conversations.append(match.conversations_id)
		# Show all message for a given conversation
		messages = []
		# user_query pulls up messages based on a match to the mes_identity column.
		# May need to sort by timestamp in the future
#		user_query = session.query(Message).filter(Message.mes_identity.contains(user))
#		for match in user_query.all():
#			messages.append(match.message)
		session.close()			
		return render_template('message.html', messageform=messageform, conversationform=conversationform, user=user, messages=messages, conversations=conversations)

	@socketio.on('conversation')
	def show_message(conversation):
#		values[conversation]
		print 'Received message from the client'
		print conversation
		conversation_id = conversation['conversation']
		print conversation_id 
		messages = []
		message_query = session.query(Message).filter_by(conversations_id=conversation_id)
		for match in message_query.all():
			messages.append(match.message)
		print messages
		emit("event", messages, broadcast = True)

#	@app.route('/chat', methods =['GET', 'POST'])
#	@login_required
#	def chat():
#		return render_template('chat.html')	

#	@app.route('/search')
#	@login_required
#	def search():
#		return render_template('search.html')

#	@app.route('/search_people-', methods=['GET', 'POST'])
#	@login_required
#	def search_people():
#		session = Session()
#		last = session.query(User).first()
#		form = RegistrationForm(obj=last)
#		session.close()
#		return render_template('search_people.html', form=form)	

	@app.route('/logout', methods=['GET', 'POST'])
	def logout():
		logout_user()
		return redirect(url_for('index'))		
	
	return app

create_app(app)

if __name__ == '__main__':
	socketio.run(app, debug=True)


