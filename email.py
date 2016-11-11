from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)




# email server
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

MAIL_USERNAME = os.environ.get('poolavannotifications')
MAIL_PASSWORD = os.environ.get('Athena12#')

# administrator list
ADMINS = ['poolavannotifications@gmail.com']

mail =Mail(app)

@app.route('/homepage')
def index():
	msg = Message('Hello', sender='thaozers@gmail.com', recipents=['thaozers@gmail.com'])
	mail.send(msg)
	return 'Message sent!'

if __name__ == '__main__':
	app.run(debug=True)