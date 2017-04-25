# Global imports
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from sqlalchemy import exists, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, query
from sqlalchemy.ext.declarative import	declarative_base
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, send, emit
from flask_bootstrap import Bootstrap


# Imports from py files
from form import RegistrationForm, LoginForm 
from model import DeclarativeBase, User, Message, Conversations, UserConversations, Interests, UserInterests

# App settings and SocketIO connection
app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:password@localhost/pythia'
app.secret_key = "6234sdfadfs78dfasd9021dsffds3baf57849sdfssdd057348905fds79340"
socketio = SocketIO(app)

def create_app(app):
	# Initialize db connection
	original_engine = create_engine('postgresql://admin:password@localhost/pythia')
	Session = sessionmaker(bind=original_engine)
	metadata = DeclarativeBase.metadata
	metadata.create_all(original_engine)
	session = Session()
	# Inititalize Flask-Login
	login_manager = LoginManager()
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(username):
		return session.query(User).get(username)

	# Routes
	#
	# Index. Allows user to login to app. Page should link to the Sign-up page
	@app.route('/', methods =['GET', 'POST'])
	def index():
		session = Session()
		signupform = RegistrationForm()
		loginform = LoginForm()
		# Check if user exists, validate credentials, then  redirect to Profile page. 
		# If validaiton fails, flash incorrect username or password
		if loginform.validate_on_submit():
			username = session.query(User).filter_by(username = loginform.lg_username.data).first()
			if username and username.password == loginform.lg_password.data:
				login_user(username)
				session.close()
				return redirect(url_for('profile', username= current_user.username, loginform=loginform))
			else:
				flash('Username or Password Incorrect')
		session.close()
		return render_template('index.html', loginform=loginform)	


	# Sign up page allows users to register for the site. 
	@app.route('/signup', methods =['GET', 'POST'])
	def signup():
		session = Session()
		signupform = RegistrationForm()
		# Register user if user data is unique / valid
		# If registration is successful, redirect to the profile page
		if signupform.validate_on_submit():
			user = User(firstname = signupform.firstname.data, lastname = signupform.lastname.data, username = signupform.username.data, email = signupform.email.data, password = signupform.password.data)
			session.add(user)
			session.commit()
			username = session.query(User).filter_by(username = signupform.username.data).first()
			login_user(username)
			session.close()
			return redirect(url_for('profile', username= current_user.username, signupform=signupform))
		session.close()
		return render_template('signup.html', signupform=signupform)	


	# Profile page for the current user
	@app.route('/profile', methods =['GET', 'POST'])	
	@login_required
	def profile():
		return render_template('profile.html', username=current_user.username)


	# Read only profile page for search feature
	@app.route('/profile/<username>', methods =['GET', 'POST'])	
	@login_required
	def read_profile(username):
		return render_template('viewprofile.html', username=username)


	# Allows for user conversations
	@app.route('/message', methods =['GET', 'POST'])
	@login_required
	def message():
		return render_template('message.html')


	# Allows the user to search for other with common interests
	@app.route('/search', methods=['GET', 'POST'])
	@login_required
	def search():
		return render_template('search.html')


	# Logout current user
	@app.route('/logout', methods=['GET', 'POST'])
	def logout():
		logout_user()
		return redirect(url_for('index'))	

	# Socket Routes
	@socketio.on('get_profileinfo')
	def get_profileinfo(get_profileinfo):
		session = Session()
		# Get username from the client
		username =  get_profileinfo['user']
		# Get the cooresponding ID for the supplied user
		user_id_list = []
		user_id = session.query(User).filter_by(username=username)
		for match in user_id.all():
			user_id_list.append(match.id)
		user_id = user_id_list[0]
		# Send a User's description and interest list to the client
		descriptions = []
		user_interests = []
		# Search the User table for a user's description
		description_query = session.query(User).filter_by(id=user_id)
		# Search the UserInterests table for interests tied to the supplied user
		interest_query = session.query(UserInterests).\
			join(Interests, UserInterests.interest_id==Interests.id).\
			add_columns(UserInterests.user_id, UserInterests.interest_id, Interests.id, Interests.interest).\
			filter(UserInterests.user_id==user_id)
		# Append interests to the interest list
		for interest in interest_query.all():
			user_interests.append(interest.interest)
		session.close()
		# Append user description to description list
		for match in description_query.all():
				descriptions.append(match.description)
		# Close session
		session.close()
		# Emit the description list + interest list to the client
		emit('load_profiledes', descriptions, broadcast=True)
		emit('load_profileint', user_interests, broadcast=True)

	# Update a profile description
	@socketio.on('profilestore')
	def profilestore(profilestore):
		user = current_user.id
		session = Session()
		# Commit the new description to the db
		profile_info = User(id = user, description = profilestore['description'])
		session.merge(profile_info)
		session.commit()
		session.close()

	# Update a user interest. 
	# Route will commit a new interest to the Interest table if interest DNE
	@socketio.on('intereststore')
	def intereststore(intereststore):
		user = current_user.id
		session = Session()
		# Create a list of interests from client supplied data
		interests = []
		for x in intereststore['interest']:
			interests.append(x)
		# Add interest to Interests table if it DNE
		for interest in interests:
			interest_exists = session.query(Interests).filter(Interests.interest==interest).all()
			if not interest_exists:
				missing_interests = Interests(interest = interest)
				session.add(missing_interests)
				session.commit()
		# Add user/interests combination to the UserInterests table if DNE
		for interest in interests:
			# Get interest IDs for supplied interests
			interest_ids = []
			get_interest_ids = session.query(Interests).filter(Interests.interest==interest)
			for interest in get_interest_ids.all():
				interest_ids.append(interest.id)
			# Check if User-Interest link exists. If not, create link
			for interest in interest_ids:
				interests_link_exists = session.query(UserInterests).\
					filter(UserInterests.interest_id==interest).\
					filter(UserInterests.user_id==current_user.id).all()
				if not interests_link_exists:
					missing_userinterests = UserInterests(user_id=current_user.id, interest_id=interest)
					session.add(missing_userinterests)
					session.commit()
		session.close()

	# Return a list of conversations for a given user
	# List is sorted by timestamp
	@socketio.on('get_conversation')
	def get_conversation():	
		session = Session()
		user = current_user.username
		timestamp = str(datetime.datetime.now())
		# Search User-Conversations table and get ID for all conversations linked to current user
		conversations = []
		conversation_query = session.query(UserConversations).filter_by(user_id=current_user.id)
		for match in conversation_query.all():
			conversations.append(match.conversations_id)
		# Take conversation IDs and find the OTHER user
		# convo_user is a list of users in conversation with the CURRENT user
		convo_user = []
		for convo in conversations:
			other_user_query = 	session.query(UserConversations).\
			join(User, UserConversations.user_id==User.id).\
			join(Conversations, UserConversations.conversations_id==Conversations.id).\
			add_columns(UserConversations.user_id, UserConversations.conversations_id, User.id, User.username, Conversations.id, Conversations.lastconvo).\
			filter(UserConversations.conversations_id==convo).\
			filter(UserConversations.user_id!=current_user.id)
			for x in other_user_query.all():
				convo_user.append({"user_id":x.username, "conversation_id":convo, "lastconvo":x.lastconvo})
		# Sort user conversations by latest conversation
		convo_user = sorted(convo_user, key=lambda item:item['lastconvo'], reverse=True)
		# Close session
		session.close()
		# Emit user list to client
		emit("userconvo", convo_user, broadcast=True)

	# Show all messages in a given conversation
	@socketio.on('conversation')
	def show_message(conversation):
		conversation_id = conversation['conversation']
		message_query = session.query(Message).join(User, Message.user_id==User.id).\
					add_columns(Message.id, Message.user_id, Message.conversations_id, Message.message, Message.timestamp, User.id, User.username).\
					filter(Message.conversations_id==conversation_id)
		messages = []
		for match in message_query.all():
			messages.append({'message':match.message, 'user_id':match.username, 'timestamp':match.timestamp})
		# Sort messages by timestamp
		messages = sorted(messages, key=lambda item:item['timestamp'])
		emit("newmessage", messages, broadcast = True)

	# Add a message to the db, then update client conversation
	@socketio.on('message')
	def archive_message(to_user,message):
		# Find id of user sending the message
		from_user = current_user.id
		timestamp = str(datetime.datetime.now())
		# Find id of user recieving the message
		foreign_user_list = []
		to_user_query = session.query(User).filter_by(username= to_user['to_user'])
		for match in to_user_query.all():
			foreign_user_list.append(match.id)
		foreign_user = foreign_user_list[0]
		# Find conversations the current user is a part of
		conversation_id = []
		conversation_id_query = session.query(UserConversations).filter_by(user_id=from_user)
		for match in conversation_id_query.all():
			conversation_id.append(match.conversations_id)
		# Find conversations shared by both users
		final_convo = []
		for convo in conversation_id:
			match = session.query(UserConversations).filter(UserConversations.user_id==foreign_user, UserConversations.conversations_id==convo)
			for conversation in match:					
				final_convo.append(conversation.conversations_id)
		# Create conversation id if one does not exist, then add message
		# If conversation already exists, just add the message
		if not final_convo:
			convo = Conversations(timestamp = timestamp, lastconvo = timestamp)
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
			session.close()
			emit("newconvo", broadcast = True)
		# If conversation already exists, just add message to db
		else:
			lastconvo = Conversations(id=final_convo[0], lastconvo = timestamp)	
			session.merge(lastconvo)
			session.commit()
			session.flush()
			message = Message(user_id=from_user, conversations_id=final_convo[0], message=message['message'], timestamp=timestamp)
			session.add(message)
			session.commit()
			session.close()
			messages = []
			# Generate a list of messages for a given conversation
			message_query = session.query(Message).join(User, Message.user_id==User.id).\
				add_columns(Message.id, Message.user_id, Message.conversations_id, Message.message, Message.timestamp, User.id, User.username).\
				filter(Message.conversations_id==final_convo[0])
			for match in message_query.all():
				messages.append({'message':match.message, 'user_id':match.username, 'timestamp':match.timestamp})
			# Sort messages by timestamp	
			messages = sorted(messages, key=lambda item:item['timestamp'])
			# Close session
			session.close()
			# Emit list of messages to the client
			emit("newmessage", messages, broadcast = True)	

	# Returns a list of users the current user has at least interest in common
	@socketio.on('get_user_match')
	def get_user_match():
		# Find users who have similar interests, based upon interest ID
		user_interests = []
		user_interests_query = session.query(UserInterests).\
			filter(UserInterests.user_id==current_user.id)
		for interest in user_interests_query.all():
			user_interests.append(interest.interest_id)
		matches = []
		for interest in user_interests:
			search = session.query(UserInterests).\
			join(User, UserInterests.user_id==User.id).\
			add_columns(UserInterests.user_id, UserInterests.interest_id, User.id, User.username).\
			filter(UserInterests.interest_id==interest)
			print search
			for x in search.all():
				if x.user_id != current_user.id and x.username not in matches:
					matches.append(x.username)
		# Close session
		session.close()	
		# Emit list of usernames		
		emit('match_list', matches, broadcast=True)


	return app

create_app(app)

if __name__ == '__main__':
	socketio.run(app, debug=True)