from flask_restful import Resource,reqparse,request
from flask import jsonify,abort
from project.models import Server,Access
from project import db
from flasgger.utils import swag_from
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_jwt_extended import create_access_token
from io import StringIO
import paramiko
import time


from Exceptions.ServersExceptions import ServerNotFoundError,AccessAlreadyExists

class GetAllGroups(Resource):
    @swag_from('project/swagger.yaml') 
    def get(self):
        all_servers = db.session.query(Server).all()
        return[server.json() for server in all_servers]
    
class CreateAccess(Resource):
    @swag_from('project/swagger.yaml') 
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Missing Username of the Access', required=True)
        self.parser.add_argument('password', type=str, help='Missing Defaut Password of the Access', required=True)
        self.parser.add_argument('server_id', type=str, help='Missing Server_id where to create the Access', required=True)
    def post(self):
        args = self.parser.parse_args()
        access_name = args['username']
        server_id = args['server_id']
        #Verify that the Server Exist by Server_id
        try:
            server = db.session().query(Server).filter_by(server_id=server_id).first()
            if not server:
                raise ServerNotFoundError(server_id)
        except ServerNotFoundError as e:
            abort(404, description=str(e))
        #Verify that the Access doesnt exist on this server
        try:
            access = db.session().query(Access).filter_by(access_name = access_name,server_id=server_id).first()
            if not access:
                raise AccessAlreadyExists(server_id)
        except ServerNotFoundError as e:
            abort(404, description=str(e))
        #create Acces on DB side

        #Create Access on Server Side
        pem_key = server.pkey.replace("\\n","\n")
        pem_key = StringIO(pem_key)
        k = paramiko.RSAKey.from_private_key(pem_key)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print ("connecting")
        c.connect( hostname = server.hostname, username = server.username, pkey = k )
        commands = [ f"sudo useradd -m {args['username']}"]
        for command in commands:
            print ("Executing {}".format( command ))
            stdin , stdout, stder = c.exec_command(command)
            print (stdout.read())
        commands = [f"sudo passwd {args['username']}\n"]
        for command in commands:
            print ("Executing {}".format( command ))
            stdin , stdout, stderr = c.exec_command(command)
            stdin.write(args['password']+"\n")
            stdin.write(args['password']+"\n")
            print (stdout.read())
        c.close()
        return {'msg': str(stderr.read().decode())}
        
    
class DeleteAccess(Resource):
    @swag_from('project/swagger.yaml') 
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Missing Username of the Access', required=True)
        self.parser.add_argument('server_id', type=str, help='Missing Server_id where to create the Access', required=True)
    def delete(self):
        args = self.parser.parse_args()
        access_name = args['username']
        server_id = args['server_id']
        server = db.session().query(Server).filter_by(server_id=server_id).first()
        try:
            server = db.session().query(Server).filter_by(server_id=server_id).first()
            if not server:
                raise ServerNotFoundError(server_id)
        except ServerNotFoundError as e:
            abort(404, description=str(e))
        user = db.session().query(Access).filter_by(access_name = access_name).first()
        #if user:
        #    return {'Error': 'Conflict',
        #            'Message': 'Access Already Exist'},409
        #else:
        pem_key = server.pkey.replace("\\n","\n")
        pem_key = StringIO(pem_key)
        k = paramiko.RSAKey.from_private_key(pem_key)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print ("connecting")
        c.connect( hostname = server.hostname, username = server.username, pkey = k )
        commands = [ f"sudo userdel -r {args['username']}"]
        for command in commands:
            print ("Executing {}".format( command ))
            stdin , stdout, stderr = c.exec_command(command)
            print (stdout.read())
        c.close()
        return {'msg': str(stderr.read().decode())}
    