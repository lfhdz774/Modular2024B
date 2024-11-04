import datetime
from io import StringIO
import re
import secrets
import string
from Exceptions.ServersExceptions import AccessAlreadyExists, ServerNotFoundError
from project import db
from flask_jwt_extended import create_access_token
import paramiko

from project.models import Access, Server


class GenerateAccess:
    def crear_usuario(self, username, server_id):
        if not self.es_nombre_usuario_valido(username):
            return {"message": f"El nombre de usuario '{username}' no es válido.", "link": ""}
        
        # Generar la contraseña automáticamente
        password = self.generar_contraseña()
        
        # Crear el usuario en el servidor
        resultado = self.crear_usuario_servidor(username, password, server_id)
        
        if resultado['exito']:
            # Crear un token JWT que contenga la contraseña
            token = self.generar_token_con_password(password)
            # Generar el enlace para que el usuario obtenga la contraseña
            enlace = f"http://localhost:3000/#/first-login/password/{token}"
            data =  {
                    "message": f"Usuario '{username}' creado con éxito. La contraseña puede ser obtenida en el siguiente enlace:",
                    "link": enlace
                    }

            return data
        else:
            return {"message":f"Error al crear el usuario: {resultado['error']}", "link": ""}

    def generar_token_con_password(self, password):
        # Crear un token JWT con la contraseña en el payload
        expires = datetime.timedelta(hours=1)  # El token expirará en 1 hora
        token = create_access_token(identity={'password': password}, expires_delta=expires)
        return token
        
    

    def generar_contraseña(self, longitud=12):
        caracteres = string.ascii_letters + string.digits + string.punctuation
        contraseña = ''.join(secrets.choice(caracteres) for i in range(longitud))
        return contraseña
    

    def crear_usuario_servidor(self, username, password, server_id):
        try:
            server = db.session().query(Server).filter_by(server_id=server_id).first()
            if not server:
                raise ServerNotFoundError(server_id)
            
            # access = db.session().query(Access).filter_by(access_name = username,server_id=server_id).first()
            # if access:
            #     raise AccessAlreadyExists(username)
            
            
            # Configuración de la conexión SSH
            pem_key = server.pkey.replace("\\n","\n")
            pem_key = StringIO(pem_key)
            k = paramiko.RSAKey.from_private_key(pem_key)
            c = paramiko.SSHClient()
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print ("connecting")
            c.connect( hostname = server.hostname, username = server.username, pkey = k )

            # Comandos para crear el usuario y establecer la contraseña
            comandos = [
                f"sudo useradd {username}",
                f"echo '{username}:{password}' | sudo chpasswd"
            ]

            for comando in comandos:
                stdin, stdout, stderr = c.exec_command(comando)
                error = stderr.read().decode()
                if error:
                    return {'exito': False, 'error': error}

            c.close()
            return {'exito': True}
        except Exception as e:
            return {'exito': False, 'error': str(e)}
        
    def es_nombre_usuario_valido(self, username):
        # Validar que solo contenga letras, números, guiones y guiones bajos
        return re.match('^[a-zA-Z0-9_-]{1,32}$', username) is not None