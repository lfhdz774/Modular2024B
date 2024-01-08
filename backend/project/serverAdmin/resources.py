from flask_restful import Resource,reqparse,request
from flask import jsonify
from project.models import Server
from project import db
from flasgger.utils import swag_from
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_jwt_extended import create_access_token

class GetAllServers(Resource):
    @swag_from('project/swagger.yaml') 
    def get(self):
        all_servers = db.session.query(Server).all()
        return[server.json() for server in all_servers]
    
class ServerAdmin(Resource):
    @swag_from('project/swagger.yaml') 
    def get(self,server_id):
        server = db.session().query(Server).filter_by(server_id=server_id).first()
        if server:
            return server.json()
        else:
            return {'server_id': 'not found'},404
    @swag_from('project/swagger.yaml') 
    def put(self,server_id):
        data = request.get_json()
        if not data:
            return {'message': 'API body is empty'}, 400
        server = db.session.get(Server,server_id)
        if server:
            if 'name' in data:
                server.name = data['name']
            if 'ip_address' in data:
                server.ip_address = data['ip_address']
            if 'port' in data:
                server.port = data['port']
            if 'username' in data:
                server.username = data['username']
            if 'password' in data:
                server.password = data['password'] ##TODO: CHECK PASSWORD ENCRYPTION
            if 'user_groups' in data:
                server.user_groups = data['user_groups']
            if 'operating_system' in data:
                server.operating_system = data['operating_system']

            db.session.commit()
            return {'message': 'User updated successfully'}, 200
        else:
            return {'server_id': 'not found'},404
        
    @swag_from('project/swagger.yaml') 
    def delete(self,server_id):
        server = db.session().query(Server).filter_by(server_id=server_id).first()
        if server:
            db.session.delete(server)
            db.session.commit()
            return {'msg' : 'Server Deleted'}
        else:
            return {'server_id': 'Server not found'},404
        
        
class AddServer(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, help='name of the Server', required=True)
        self.parser.add_argument('ip_address', type=str, help='ip_address of the Server', required=True)
        self.parser.add_argument('port', type=str, help='port of the Server', required=True)
        self.parser.add_argument('username', type=str, help='username of the Server', required=True)
        self.parser.add_argument('password', type=str, help='password of the Server', required=True)
        #self.parser.add_argument('user_groups', type=list, action='append', help='user_groups of the Server', required=True)
        self.parser.add_argument('operating_system', type=str, help='OS in the application of the Server', required=True)

    @swag_from('project/swagger.yaml')
    def post(self):
        args = self.parser.parse_args()
        data = request.get_json()
        name = args['name']
        ip_address = args['ip_address']
        port = args['port']
        username = args['username']
        password = args['password']
        user_groups = data['user_groups']
        #user_groups = [1,2,3,4,5]
        print(user_groups)
        operating_system = args['operating_system']
        server = Server(name,ip_address,port,username,password,user_groups,operating_system)
        db.session.add(server)
        db.session.commit()
        return {'msg': 'Servers Added'}