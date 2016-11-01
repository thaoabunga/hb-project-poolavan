from flask import Flask
app = Flask(__name__)

# test route
@app.route('/')
def hello_world():
	"""Homepage"""
    return 'Hello, World!'
