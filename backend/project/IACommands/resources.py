import re
import unicodedata
from flask_restful import Resource, reqparse
from flask import abort, session
from flask_jwt_extended import jwt_required
import joblib
import spacy
from spacy.matcher import Matcher
from project.GenerateAccess.GenerateAccess import GenerateAccess

class ProcesarComando(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('comando', type=str, help='Comando en lenguaje natural', required=True)
        # Load the intent classification model
        self.modelo_intenciones = joblib.load('Clasificación de intenciones/modelo_intenciones.pkl')
        # Load the spaCy Spanish model
        self.nlp = spacy.load('Clasificación de intenciones/modelo_ner')


    @jwt_required()
    def post(self):
        try:
            args = self.parser.parse_args()
            comando = args['comando']
            respuesta = None

            if 'pending_data' in session:
                print("Pending action:", session['pending_data'])
                # Hay una acción pendiente; usar el comando proporcionado como la información faltante
                missing_info = comando.strip()
                # Recuperar los datos pendientes
                datos = session.pop('pending_data')

                # Dependiendo de qué información faltaba, asignarla
                for info in datos['informacion_faltante']:
                    if info == 'employee_code':
                        datos['employee_code'] = missing_info
                    elif info == 'server':
                        datos['server'] = missing_info

                # Validar si aún falta información
                datos['informacion_faltante'] = []
                if not datos['employee_code']:
                    datos['informacion_faltante'].append('employee_code')
                if not datos['server'] and self.intencion_requiere_entidad(datos['accion'], 'server'):
                    datos['informacion_faltante'].append('server')

                if datos['informacion_faltante']:
                    # Aún falta información
                    session['pending_data'] = datos
                    return {"message": f"No pude detectar {', '.join(datos['informacion_faltante'])}. Por favor, proporcione la información faltante.", "link": ""}
                else:
                    # Proceder con la acción
                    respuesta = self.ejecutar_accion(datos)
            else:
                # No hay acción pendiente; procesar el comando normalmente
                respuesta = self.analizar_comando(comando)

            print("Respuesta:", respuesta)
            return {'respuesta': respuesta}, 200
        except Exception as e:
            abort(400, description=str(e))

    def analizar_comando(self, comando):
        # Predecir la intención
        intencion = self.modelo_intenciones.predict([comando])[0]
        datos = {
            'accion': intencion,
            'employee_code': None,
            'server': None,
            'informacion_faltante': []
        }
        
        print("Intención detectada:", intencion)
        # Procesar el comando con spaCy
        doc = self.nlp(comando)

        # Extraer entidades
        employee_codes = [ent.text for ent in doc.ents if ent.label_ == 'EMPLOYEE_CODE']
        servers = [ent.text for ent in doc.ents if ent.label_ == 'SERVER']

        print("Códigos de empleado detectados:", employee_codes)
        print("Servidores detectados:", servers)
        if employee_codes:
            codigo_empleado = self.normalizar(employee_codes[0])
            if self.es_codigo_empleado_valido(codigo_empleado):
                datos['employee_code'] = codigo_empleado
            else:
                datos['informacion_faltante'].append('employee_code')
        else:
            # Si la intención requiere 'employee_code', agregar a 'informacion_faltante'
            if self.intencion_requiere_entidad(intencion, 'employee_code'):
                datos['informacion_faltante'].append('employee_code')

        if servers:
            datos['server'] = servers[0]
        else:
            # Si la intención requiere 'server', agregar a 'informacion_faltante'
            if self.intencion_requiere_entidad(intencion, 'server'):
                datos['informacion_faltante'].append('server')

        if datos['informacion_faltante']:
            session['pending_data'] = datos
            print("Pending action:", session['pending_data'])
            return {"message": f"No pude detectar {', '.join(datos['informacion_faltante'])}. Por favor, proporcione la información faltante.", "link": ""}
        else:
            # Proceder con la acción
            return self.ejecutar_accion(datos)

    def ejecutar_accion(self, datos):
        if datos['accion'] == 'crear_usuario':
            if datos['employee_code'] and datos['server']:
                #generate_access_instance = GenerateAccess()
                #return generate_access_instance.crear_usuario(datos['employee_code'], datos['server'])
                print("Creando usuario...")
                return {"message": f"Usuario creado para el código de empleado {datos['employee_code']} en el servidor {datos['server']}.", "link": ""}
            else:
                return {"message": "Faltan datos para crear el usuario.", "link": ""}
        elif datos['accion'] == 'info_usuario':
            if datos['employee_code']:
                return self.consultar_usuario(datos['employee_code'])
            else:
                return {"message": "Falta el código de empleado para consultar la información.", "link": ""}
        else:
            return {"message": "Acción no reconocida.", "link": ""}

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

    def es_nombre_usuario_valido(self, username):
        # Validar que solo contenga letras, números, guiones y guiones bajos
        return re.match('^[a-zA-Z0-9_-]{1,32}$', username) is not None

    def es_codigo_empleado_valido(self, codigo):
        # Validar que el código de empleado sea un número de 4 dígitos
        return re.match('^\d{4}$', codigo) is not None

    