from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_required
from config import Config
import os


db = SQLAlchemy()
app = Flask(__name__)


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(app):
	app.config.from_object(os.environ['APP_SETTINGS'])
	db.init_app(app)

	@app.route('/')
	def index():
		return render_template('index.html')

	@app.route('/signup', methods=['GET', 'POST'])
	def sign_up():
		form = LoginForm()
		if form.validate_on_submit():
			user = User.query.filter_by(email=form.email.data).first()
			if user is not None and user.verify_password(form.password.data):
				login_user(user, form.remember_me.data)
				return redirect(request.args.get('next') or url_for('main.index'))
			flash('Invalid username or password.')
		return render_template('signup.html')

	@app.route('/about')
	def about():
		return render_template('about.html')

	@app.route('/search')
	@login_required
	def search():
		return render_template('search.html')

	@app.route('/profile')
	@login_required
	def profile():
		return render_template('profile.html')


	login_manager.init_app(app)	

	return app

create_app(app)	



if __name__ == '__main__':
	app.run()


