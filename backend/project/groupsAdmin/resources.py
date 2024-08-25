from flask_restful import Resource,reqparse,request
from flask import jsonify
from project.models import Group,Server
from project import db
from flasgger.utils import swag_from
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_jwt_extended import create_access_token

class GetAllGroups(Resource):
    @swag_from('project/swagger.yaml') 
    def get(self):
        all_servers = db.session.query(Server).all()
        return[server.json() for server in all_servers]
    
class GroupAdmin(Resource):
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
        
        
class AddGroup(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('group_name', type=str, help='name of the Group', required=True)
        self.parser.add_argument('description', type=str, help='description of the Group', required=True)
        self.parser.add_argument('server_id', type=str, help='port of the Server', required=True)

    @swag_from('project/swagger.yaml')
    def post(self):
        args = self.parser.parse_args()
        group_name = args['group_name']
        description = args['description']
        server_id = args['server_id']
        existing_server = Server.query.get(server_id)
        if existing_server:
            new_group = Group()(group_name,description,server_id)
            db.session.add(new_group)
            db.session.commit()
            return {'msg': 'Servers Added'},200
        else:
            return {'msg': 'Server_id does not exist'},404
