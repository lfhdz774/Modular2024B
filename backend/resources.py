from flask_restful import Resource,reqparse
from flask import jsonify
from project.models import User
from project import db
from flasgger.utils import swag_from
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_jwt_extended import create_access_token

class Signup(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Username of the user', required=True)
        self.parser.add_argument('password', type=str, help='Password of the user', required=True)

    @swag_from('project/swagger.yaml') 
    def get(self):
        args = self.parser.parse_args()
        username = args['username']
        user = db.session().query(User).filter_by(username).first()
        if user:
            return user.json()
        else:
            return {'username': 'not found'},404
    
    @swag_from('project/swagger.yaml')
    def post(self):
        args = self.parser.parse_args()
        username = args['username']
        password = args['password']
        user = User(username,password)
        db.session.add(user)
        db.session.commit()
        #return {'User Added'}

    @swag_from('project/swagger.yaml') 
    def delete(self,id):
        user = db.session().query(User).filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        #return {'User Deleted'}

class Login(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Username of the user', required=True)
        self.parser.add_argument('password', type=str, help='Password of the user', required=True)

    @swag_from('project/swagger.yaml') 
    def post(self):
        args = self.parser.parse_args()
        username = args['username']
        password = args['password']
        user = db.session().query(User).filter_by(username=username).first()
        print(user)
        if username == "test" and password == "test":
            access_token = create_access_token(identity=username)
            return {'access_token': access_token}
        else:
            return {'message': 'Invalid username or password'}, 401


class AllUsersResource(Resource):
    @swag_from('project/swagger.yaml') 
    def get(self):
        all_users = db.session.query(User).all()
        return[user.json() for user in all_users]
        
    
class getUser(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Username of the user', required=True)
    @swag_from('project/swagger.yaml') 
    def get(self):
        args = self.parser.parse_args()
        username = args['username']
        user = db.session().query(User).filter_by(username = username).first()
        if user:
            return user.json()
        else:
            return {'username': 'not found'},404