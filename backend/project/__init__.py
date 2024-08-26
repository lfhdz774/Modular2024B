from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from dotenv import load_dotenv
# Load environment variables from .flaskenv file
load_dotenv('.flaskenv')

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

swagger = Swagger(app, template_file='swagger.yaml')

PGUSER = os.getenv('PGUSER')
PGPASSWORD = os.getenv('PGPASSWORD')
app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{PGUSER}:{PGPASSWORD}@ep-broad-moon-a53iqxig.us-east-2.aws.neon.tech/serverportaldb?options=project%3Dep-broad-moon-a53iqxig&sslmode=require'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
Migrate(app,db)

from project.login.view import login_blueprint
from project.serverConnection.view import serverConnection_blueprint
#from project.serverAdmin.view import serverAdmin_blueprint

app.register_blueprint(login_blueprint)
app.register_blueprint(serverConnection_blueprint)
#app.register_blueprint(serverAdmin_blueprint)