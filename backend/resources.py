from flask_restful import Resource,reqparse
from project.models import User
from project import db

class Signup(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Username of the user', required=True)
        self.parser.add_argument('password', type=str, help='Password of the user', required=True)

    def get(self):
        args = self.parser.parse_args()
        username = args['username']
        user = db.session().query(User).filter_by(username).first()
        if user:
            return user.json()
        else:
            return {'username': 'not found'},404
        
    def post(self):
        args = self.parser.parse_args()
        username = args['username']
        password = args['password']
        user = User(username,password)
        db.session.add(user)
        db.session.commit()
        #return {'User Added'}

    def delete(self,id):
        user = db.session().query(User).filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        #return {'User Deleted'}

class AllUsersResource(Resource):
    def get(self):
        all_users = db.session.query(User).all()
        return[user.json() for user in all_users]

class AllUsersResource(Resource):
    def get(self):
        all_users = db.session.query(User).all()
        return[user.json() for user in all_users]
        
    
class getUser(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Username of the user', required=True)
    def get(self):
        args = self.parser.parse_args()
        username = args['username']
        print (username)
        user = db.session().query(User).filter_by(username = username).first()
        if user:
            return user.json()
        else:
            return {'username': 'not found'},404