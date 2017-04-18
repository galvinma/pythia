# Global imports
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from sqlalchemy import exists, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, query
from sqlalchemy.ext.declarative import	declarative_base
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, send, emit

# Imports from py files
from form import RegistrationForm, LoginForm 
from model import DeclarativeBase, User, Message, Conversations, UserConversations, Interests, UserInterests

# App settings and SocketIO connection
app = Flask(__name__)
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
			username = session.query(User).filter_by(username = loginform.logusername.data).first()
			if username and username.password == loginform.logpassword.data:
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
		loginform = LoginForm()
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
		return render_template('signup.html', signupform=signupform, loginform=loginform)	


	# Profile page for the current user
	@app.route('/profile', methods =['GET', 'POST'])	
	@login_required
	def profile():
		return render_template('profile.html', username=current_user.username)


	# Read only profile page for search feature
	@app.route('/profile/<username>', methods =['GET', 'POST'])	
	@login_required
	def read_profile(username):
		return render_template('read_profile.html', username=username)


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


	return app

create_app(app)

if __name__ == '__main__':
	socketio.run(app, debug=True)