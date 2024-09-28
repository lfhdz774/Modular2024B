from flask_restful import Resource,reqparse,request
from flask import jsonify,abort
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
    
class GetServer(Resource):
    def __init__(self) -> None:
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('server_id', type=int, help='ID of the server', required=True)

    @swag_from('project/swagger.yaml') 
    def get(self,server_id):
        server = db.session().query(Server).filter_by(server_id=server_id).first()
        if server:
            return server.json()
        else:
            return {'server_id': 'not found'},404
        
class AddServer(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, help='name of the Server', required=True)
        self.parser.add_argument('hostname', type=str, help='hostname of the Server', required=True)
        self.parser.add_argument('ip_address', type=str, help='ip_address of the Server', required=True)
        self.parser.add_argument('username', type=str, help='username of the Server', required=True)
        self.parser.add_argument('pkey', type=str, help='pkey of the Server', required=True)
        #self.parser.add_argument('user_groups', type=list, action='append', help='user_groups of the Server', required=True)
        self.parser.add_argument('operating_system', type=str, help='OS in the application of the Server', required=True)

    @swag_from('project/swagger.yaml')
    def post(self):
        try:
            args = self.parser.parse_args()
            #data = request.get_json()
            name = args['name']
            hostname = args['hostname']
            ip_address = args['ip_address']
            username = args['username']
            pkey = args['pkey']
            #user_groups = data['user_groups']
            #user_groups = [1,2,3,4,5]
            operating_system = args['operating_system']
            server = Server(name,hostname,ip_address,username,pkey,operating_system)
            db.session.add(server)
            db.session.commit()
            return {'msg': 'Server Added'}
        except Exception as e:
            abort(808, description="Server not Found")
        
    
class DeleteServer(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        args = self.parser.parse_args()
        print("Datos recibidos:", args)
        self.parser.add_argument('server_id', type=str, help='Server_id of the Server', required=True)
    @swag_from('project/swagger.yaml') 
    def delete(self):
        args = self.parser.parse_args()
        server_id = args['server_id']
        try:
            server = db.session().query(Server).filter_by(server_id=server_id).first()
            db.session.delete(server)
            db.session.commit()
            return {'msg' : 'Server Deleted'}
        except Exception as e:
            abort(404, description="Server not Found")

class UpdateServer(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('server_id', type=str, help='Server_id of the Server', required=True)
        self.parser.add_argument('updates', type=dict, help='Json object with the fields to update', required=True)
    @swag_from('project/swagger.yaml') 
    def put(self):
            args = self.parser.parse_args()
            server_id = args['server_id']
            updates = args['updates']
            # Find the server
            server = db.session().query(Server).filter_by(server_id=server_id).first()
            if not server:
                return {'message': 'Server not found'}, 404
            # Validate pkey if it's being updated
            if 'pkey' in updates:
                for field, value in updates.items():
                    setattr(server, field, value)
            elif 'hostname' in updates:
                for field, value in updates.items():
                    setattr(server, field, value)
            elif 'ip_address' in updates:
                for field, value in updates.items():
                    setattr(server, field, value)
            elif 'username' in updates:
                for field, value in updates.items():
                    setattr(server, field, value)
            elif 'name' in updates:
                for field, value in updates.items():
                    setattr(server, field, value)
            else:
                return {'message': 'Property not available for update'}, 405
            
            db.session().commit()
            return {'message': 'Server updated successfully'}, 200

