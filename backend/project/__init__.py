from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from dotenv import load_dotenv
# Load environment variables from .flaskenv file
load_dotenv('.flaskenv')

from Exceptions.BaseCustomError import BaseCustomError


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

swagger = Swagger(app, template_file='swagger.yaml')

PGUSER = os.getenv('PGUSER')
PGPASSWORD = os.getenv('PGPASSWORD')

app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{PGUSER}:{PGPASSWORD}@ep-broad-moon-a53iqxig.us-east-2.aws.neon.tech/serverportaldb?sslmode=require'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app,db)

@app.errorhandler(BaseCustomError)
def handle_custom_exception(error):
    response = jsonify({'msg': error.message})
    response.status_code = error.code
    return response

from project.login.view import login_blueprint
from project.serverAdmin.view import serverAdmin_blueprint
from project.User.view import user_blueprint
from project.Signup.view import signup_blueprint

app.register_blueprint(signup_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(serverConnection_blueprint)
#app.register_blueprint(serverAdmin_blueprint)