from flask import Flask
app = Flask(__name__)

# test route
@app.route('/')
def hello_world():
    return 'Hello, World!'
