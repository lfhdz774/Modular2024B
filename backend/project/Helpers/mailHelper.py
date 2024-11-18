# importing libraries 
from flask import Flask 
from flask_mail import Mail, Message 
from dotenv import load_dotenv
import os

# Load environment variables from .flaskenv file
load_dotenv('.flaskenv')

   
app = Flask(__name__) 
   
# configuration of mail 
app.config['MAIL_SERVER']='email-smtp.us-east-2.amazonaws.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = PGUSER = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = PGUSER = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

app.config['MAIL_DEBUG'] = True

mail = Mail(app) 


def send_email(subject, body, recipient):
    with app.app_context():
        msg = Message(subject, sender='serverportalapp@gmail.com', recipients=[recipient])
        msg.html = body
        try:
            mail.send(msg)
            return True
        except Exception as e:
            print("Error al enviar el correo:", e)
            return False