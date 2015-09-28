from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from model import Result

@app.route('/')
def text():
		return "Welcome to the Pythia Project!"


if __name__ == '__main__':
	app.run()


