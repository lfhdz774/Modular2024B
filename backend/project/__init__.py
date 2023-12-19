from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app, template_file='swagger.yaml')

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://vanhxpev:ekq-InJ8Vr26kOHoCGhaXRnOmP-VzSiz@bubble.db.elephantsql.com/vanhxpev'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app,db)

from project.login.view import login_blueprint

app.register_blueprint(login_blueprint,url_prefix='/login')