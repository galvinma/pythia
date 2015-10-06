import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import Form
from wtforms.fields import BooleanField, StringField, SubmitField
from wtforms.validators import Required



from form import RegistrationForm


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SECRET_KEY'] = 'secret'


def create_app(app):

	@app.route('/')
	def index():
		return render_template('index.html')

	@app.route('/signup', methods=['GET', 'POST'])
	def sign_up():
		form = RegistrationForm()
		if form.validate_on_submit():
			return redirect(url_for('profile'))
		return render_template('signup.html', form=form)



	@app.route('/search')
	def search():
		return render_template('search.html')

	@app.route('/profile')
	def profile():
		return render_template('profile.html')
	

	return app

create_app(app)	



if __name__ == '__main__':
	app.run()


