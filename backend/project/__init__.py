from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity
from flask_cors import CORS
import os
import nltk
from dotenv import load_dotenv
from flask_session import Session


# Load environment variables from .flaskenv file
load_dotenv('.flaskenv')
import os
from dotenv import load_dotenv
# Load environment variables from .flaskenv file
load_dotenv('.flaskenv')

from Exceptions.BaseCustomError import BaseCustomError


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this!
jwt = JWTManager(app)

Session(app)

CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}})

swagger = Swagger(app, template_file='swagger.yaml')

PGUSER = os.getenv('PGUSER')
PGPASSWORD = os.getenv('PGPASSWORD')
app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{PGUSER}:{PGPASSWORD}@ep-broad-moon-a53iqxig.us-east-2.aws.neon.tech/serverportaldb?options=project%3Dep-broad-moon-a53iqxig&sslmode=require'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
Migrate(app,db)

# Download NLTK data
nltk.download('punkt')
nltk.download('punkt_tab')

# Añadimos los handles de errores  para los errores de JWT
@jwt.invalid_token_loader
def invalid_token_callback(callback):
    return jsonify({
        'error': 'Invalid session',
        'message': 'The token is invalid or expired',
        'code': 769
    }), 769


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'error': 'Invalid session',
        'message': 'The token has expired',
        'code': 769
    }), 769


@jwt.unauthorized_loader
def missing_token_callback(callback):
    return jsonify({
        'error': 'Invalid session',
        'message': 'Token is missing',
        'code': 769
    }), 769


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'error': 'Invalid session',
        'message': 'The token has been revoked',
        'code': 769
    }), 769


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'error': 'Invalid session',
        'message': 'The token is not fresh',
        'code': 769
    }), 769

@app.errorhandler(BaseCustomError)
def handle_custom_exception(error):
    response = jsonify({'msg': error.message})
    response.status_code = error.code
    return response

# Añadimos un decorador para verificar el JWT en todas las rutas excepto en la de login
@app.before_request
def check_jwt():
    #log a message with the name of the endpoint
    print(request.endpoint)
    if request.endpoint != 'login.login':
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({
                'error': 'Invalid session',
                'message': str(e),
                'code': 769
            }), 769

from project.login.view import login_blueprint
from project.serverConnection.view import serverConnection_blueprint
#from project.serverAdmin.view import serverAdmin_blueprint
from project.User.view import user_blueprint
from project.Signup.view import signup_blueprint
from project.IACommands.view import iaCommands_blueprint
from project.PasswordManagement.view import PasswordView_blueprint
from project.Servers.view import servers_blueprint
from project.Reports.view import reports_blueprint

app.register_blueprint(signup_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(servers_blueprint)
app.register_blueprint(serverConnection_blueprint)
app.register_blueprint(iaCommands_blueprint)
app.register_blueprint(PasswordView_blueprint)
app.register_blueprint(reports_blueprint)