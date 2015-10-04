from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

login_manager = LoginManager
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def sign_up():
	return render_template('signup.html')

@app.route('/search')
def search():
	return render_template('search.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/profile')
def profile():
	return render_template('profile.html')

@app.route('/test')
def test():
	return render_template('test.html')

if __name__ == '__main__':
	app.run()


