from flask import Flask
app = Flask(__name__)


@app.route('/')
def text():
		return "Welcome to the Pythia Project!"

if __name__ == '__main__':
	app.run()