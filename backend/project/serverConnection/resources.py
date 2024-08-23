from flask_restful import Resource,reqparse,request
from flask import jsonify
from project.models import Group,Server
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
    def get(self):
        k = paramiko.RSAKey.from_private_key_file("project/serverConnection/key11.pem")
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print ("connecting")
        c.connect( hostname = "ec2-3-145-177-3.us-east-2.compute.amazonaws.com", username = "ubuntu", pkey = k )
        print ("connected")
        commands = [ "sudo useradd serverportaltest2","sudo passwd serverportaltest2"]

        for command in commands:
            print ("Executing {}".format( command ))
            stdin , stdout, stderr = c.exec_command(command)
            stdin.write('newpw\n')
            stdin.write('newpw\n')
            print (stdout.read())
            print( "Errors")
            return {'msg': str(stderr.read())}
        c.close()
    