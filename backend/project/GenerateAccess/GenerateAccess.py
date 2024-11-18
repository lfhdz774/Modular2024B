import datetime
from io import StringIO
import re
import secrets
import string
from Exceptions.ServersExceptions import AccessAlreadyExists, ServerNotFoundError
from project import db
from flask_jwt_extended import create_access_token
import paramiko
import random
from flask_mail import Mail, Message

from project.models import Access, Server
from ..Helpers.mailHelper import send_email

from project.models import Access, Server


class GenerateAccess:
    def crear_usuario(self, username, server_id, email):
        if not self.es_nombre_usuario_valido(username):
            return {"message": f"El nombre de usuario '{username}' no es válido.", "link": ""}
        
        # Generar la contraseña automáticamente
        password = self.generar_contraseña()


         # Crear un token JWT que contenga la contraseña
        token = self.generar_token_con_password(password)

        # Crear el usuario en el servidor
        resultado = self.crear_usuario_servidor(username, password, server_id)
        
        if resultado['exito']:
            # Crear un token JWT que contenga la contraseña
            token = self.generar_token_con_password(password)
            # Generar el enlace para que el usuario obtenga la contraseña
            enlace = f"http://serverportal-app.org/#/first-login/password/{token}"

            htmlBody = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            color: #333333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 20px;
            text-align: center;
        }}
        .header {{
            background-color: #042174;
            padding: 20px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            color: #ffffff;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .message {{
            margin: 20px 0;
            font-size: 16px;
            color: #555555;
        }}
        .button {{
            background-color: #042174;
            color: #ffffff;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            font-size: 16px;
            display: inline-block;
        }}
        .footer {{
            margin-top: 20px;
            font-size: 12px;
            color: #aaaaaa;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Bienvenido a nuestro sistema</h1>
        </div>
        <div class="message">
            <p>Se ha creado un usuario para usted en el servidor.</p>
            <p>Para acceder y ver su contraseña, haga clic en el enlace a continuación:</p>
            <a href="{enlace}" class="button">Obtener contraseña</a>
        </div>
        <div class="footer">
            <p>Si tiene alguna pregunta, no dude en ponerse en contacto con nuestro equipo de soporte.</p>
            <p>Gracias por unirse a nosotros.</p>
        </div>
    </div>
</body>
</html>
"""




            send_email("Contraseña de acceso", htmlBody, email)




            data =  {
                    "result" : True,
                    "message": f"Usuario creado exitosamente, la contraseña ha sido enviada al correo electrónico del empleado para que pueda obtener su contraseña."
                    }

            return data
        else:
            return {"result" : False,"message":f"Error al crear el usuario: {resultado['error']}"}

    def generar_token_con_password(self, password):
        # Crear un token JWT con la contraseña en los additional_claims
        expires = datetime.timedelta(hours=1)  # El token expirará en 1 hora
        additional_claims = {'password': password}
        token = create_access_token(identity='', expires_delta=expires, additional_claims=additional_claims)
        print('Token generado:', token)
        return token
        
    

    def generar_contraseña(self, longitud=12):
        caracteres = string.ascii_letters + string.digits + string.punctuation
        contraseña = ''.join(secrets.choice(caracteres) for i in range(longitud))
        return contraseña
    
    def generar_username(self, data):
        print(data)
        username = data[0] + data[1] + str(random.randint(10,99))
        return username

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
            print ("closing")
            return {'exito': True}
        except Exception as e:
            return {'exito': False, 'error': str(e)}
        
    def es_nombre_usuario_valido(self, username):
        # Validar que solo contenga letras, números, guiones y guiones bajos
        return re.match('^[a-zA-Z0-9_-]{1,32}$', username) is not None