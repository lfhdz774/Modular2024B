import datetime
import secrets
import string
import re
import unicodedata
from flask_restful import Resource, reqparse
from flask import abort, session
from flask_jwt_extended import create_access_token, jwt_required
import paramiko
import joblib
import spacy
from spacy.matcher import Matcher

class ProcesarComando(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('comando', type=str, help='Comando en lenguaje natural', required=True)
        # Load the intent classification model
        self.modelo_intenciones = joblib.load('Clasificación de intenciones/modelo_intenciones.pkl')
        # Load the spaCy Spanish model
        self.nlp = spacy.load('es_core_news_sm')
        # Configure the Matcher
        self.matcher = Matcher(self.nlp.vocab)
        self.configurar_patrones()
        
    def configurar_patrones(self):
        # Define patterns
        pattern_llamado = [
            {'LEMMA': {'IN': ['crear', 'agregar', 'generar', 'añadir', 'registrar']}},
            {'LOWER': {'IN': ['usuario', 'acceso', 'cuenta']}},
            {'LOWER': {'IN': ['llamado', 'llamada', 'nombrado', 'como']}},
            {'IS_ALPHA': True, 'OP': '+'}
        ]
        pattern_para = [
            {'LEMMA': {'IN': ['crear', 'agregar', 'generar', 'añadir', 'registrar']}},
            {'LOWER': {'IN': ['usuario', 'acceso', 'cuenta']}},
            {'LOWER': 'para'},
            {'IS_ALPHA': True, 'OP': '+'}
        ]
        self.matcher.add('USERNAME', [pattern_llamado, pattern_para])

    @jwt_required()
    def post(self):
        try:
            args = self.parser.parse_args()
            comando = args['comando']
            respuesta = None
            try:
                print("Pending action:", session['pending_data'])
            except:
                print("No hay pending action")
                pass
            if 'pending_data' in session:
                print("Pending action:", session['pending_data'])
                # There is a pending action; use the provided command as the missing information
                missing_info = comando.strip()
                # Retrieve the pending data
                datos = session.pop('pending_data')
                datos['username'] = self.normalizar(missing_info)
                # Validate the username
                if not self.es_nombre_usuario_valido(datos['username']):
                    respuesta = {"message":f"El nombre de usuario '{datos['username']}' no es válido. Por favor, proporcione un nombre de usuario válido.", "link": ""}
                    # Keep the pending action in the session
                    session['pending_action'] = datos['accion']
                    session['pending_data'] = datos
                else:
                    session.clear()
                    # Proceed with the action
                    respuesta = self.ejecutar_accion(datos)
            else:
                # No pending action; process the command normally
                respuesta = self.analizar_comando(comando)

            return {'respuesta': respuesta}, 200
        except Exception as e:
            abort(400, description=str(e))

    def analizar_comando(self, comando):
        # Predict the intent
        intencion = self.modelo_intenciones.predict([comando])[0]
        datos = {
            'accion': intencion,
            'username': None,
            'informacion_faltante': []
        }
        
        # Process the command with spaCy
        doc = self.nlp(comando)

        # Extract the username using NER
        nombres = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
        if nombres:
            datos['username'] = self.normalizar(nombres[0])
        else:
            # Use additional methods
            datos['username'] = self.extraer_username_con_matcher(doc)
            if not datos['username']:
                datos['username'] = self.extraer_username_con_regex(comando)
        
        if not datos['username']:
            # Missing username; prompt the user
            datos['informacion_faltante'].append('username')
            session['pending_data'] = datos
            print("Pending action:", session['pending_data'])
            return {"message":"No pude detectar el nombre de usuario. Por favor, proporcione el nombre de usuario.", "link": ""}
        else:
            # Proceed with the action
            return self.ejecutar_accion(datos)

    def ejecutar_accion(self, datos):
        if datos['accion'] == 'crear_usuario':
            return self.crear_usuario(datos['username'])
        elif datos['accion'] == 'eliminar_usuario':
            return self.eliminar_usuario(datos['username'])
        elif datos['accion'] == 'consultar_usuario':
            return self.consultar_usuario(datos['username'])
        else:
            return {"message":"Acción no reconocida.", "link": ""}

    def extraer_username_con_matcher(self, doc):
        matches = self.matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            print(f"Matcher encontró el span: '{span.text}'")
            username_tokens = [token.text for token in span[1:] if token.is_alpha]
            if username_tokens:
                username = self.normalizar(' '.join(username_tokens))
                print(f"Nombre de usuario extraído con Matcher: {username}")
                return username
        return None

    def extraer_username_con_regex(self, comando):
        patrones_nombre = [
            r"\b(?:para|llamado|llamada|nombrado|como)\b\s+(\w+)",
        ]
        for patron in patrones_nombre:
            match = re.search(patron, comando, re.IGNORECASE)
            if match:
                username = self.normalizar(match.group(1))
                print(f"Nombre de usuario extraído con Regex: {username}")
                return username
        return None

    def extraer_username_con_ner(self, doc):
        # Utilizar el NER predefinido para entidades de tipo PERSON
        nombres = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
        if nombres:
            return self.normalizar(nombres[0])
        else:
            print(doc.ents)
            nombres = [token.text for token in doc if token.pos_ == 'PROPN']
            print("Nombres de usuario detectados con NER:", nombres)
            if nombres:
                return self.normalizar(nombres[0])
        return None

    def normalizar(self, texto):
        texto_normalizado = ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )
        return texto_normalizado.lower()

    def normalizar(self, texto):
        texto_normalizado = ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )
        return texto_normalizado.lower()

    def crear_usuario(self, username):
        if not self.es_nombre_usuario_valido(username):
            return {"message": f"El nombre de usuario '{username}' no es válido.", "link": ""}
        
        # Generar la contraseña automáticamente
        password = self.generar_contraseña()
        
        # Crear el usuario en el servidor
        resultado = self.crear_usuario_servidor(username, password)
        
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
        
    def es_nombre_usuario_valido(self, username):
        # Validar que solo contenga letras, números, guiones y guiones bajos
        return re.match('^[a-zA-Z0-9_-]{1,32}$', username) is not None

    def generar_contraseña(self, longitud=12):
        caracteres = string.ascii_letters + string.digits + string.punctuation
        contraseña = ''.join(secrets.choice(caracteres) for i in range(longitud))
        return contraseña
    

    def crear_usuario_servidor(self, username, password):
        try:
            # Configuración de la conexión SSH
            k = paramiko.RSAKey.from_private_key_file("project/serverConnection/key11.pem")
            c = paramiko.SSHClient()
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.connect( hostname = "ec2-3-16-48-222.us-east-2.compute.amazonaws.com", username = "ubuntu", pkey = k )

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