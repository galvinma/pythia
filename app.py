from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

@app.route('/')
def text():
    return render_template('index.html')

@app.route('/register')
def sign_up():
		return "There will be a signup page here!"

if __name__ == '__main__':
	app.run()


