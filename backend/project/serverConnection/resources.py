from flask_restful import Resource,reqparse,request
from flask import jsonify
from project.models import Server,Access
from project import db
from flasgger.utils import swag_from
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_jwt_extended import create_access_token
import paramiko


class GetAllGroups(Resource):
    @swag_from('project/swagger.yaml') 
    def get(self):
        all_servers = db.session.query(Server).all()
        return[server.json() for server in all_servers]
    
class CreateId(Resource):
    @swag_from('project/swagger.yaml') 
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Username of the user', required=True)
        self.parser.add_argument('password', type=str, help='Defaut Password of the user', required=True)
    def post(self):
        args = self.parser.parse_args()
        access_name = args['username']
        user = db.session().query(Access).filter_by(access_name = access_name).first()
        if user:
            return {'Error': 'Conflict',
                    'Message': 'User Already Exist'},409
        else:
            k = paramiko.RSAKey.from_private_key_file("project/serverConnection/key11.pem")
            c = paramiko.SSHClient()
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print ("connecting")
            c.connect( hostname = "ec2-3-16-48-222.us-east-2.compute.amazonaws.com", username = "ubuntu", pkey = k )
            print('connected')
            commands = [ "sudo useradd "+ args['username'],"sudo passwd "+ args['username']]
            for command in commands:
                print ("Executing {}".format( command ))
                stdin , stdout, stderr = c.exec_command(command)
                stdin.write("sudo passwd " + args['username'])
                stdin.write(args['password']+"\n")
                stdin.write(args['password']+"\n")
                stdin.flush()
                print (stdout.read())
                print( "Errors")
                return {'msg': str(stderr.read().decode())}
        c.close()

class DeeteUser(Resource):
    def __inin__(self):
        self.parser = self.parser = reqparse.RequestParser()
        self.parser.add_argument('user_id', type=str, help='Required user_id of the user', required=True)
    