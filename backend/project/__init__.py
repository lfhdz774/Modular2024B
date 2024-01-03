from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from Exceptions.BaseCustomError import BaseCustomError


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

swagger = Swagger(app, template_file='swagger.yaml')

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://vanhxpev:ekq-InJ8Vr26kOHoCGhaXRnOmP-VzSiz@bubble.db.elephantsql.com/vanhxpev'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app,db)

@app.errorhandler(BaseCustomError)
def handle_custom_exception(error):
    response = jsonify({'msg': error.message})
    response.status_code = error.code
    return response


from project.login.view import login_blueprint

app.register_blueprint(login_blueprint)