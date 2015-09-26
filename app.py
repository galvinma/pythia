from flask import Flask
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route('/')
def text():
		return "Welcome to the Pythia Project!"

print(os.environ['APP_SETTINGS'])

if __name__ == '__main__':
	app.run()


