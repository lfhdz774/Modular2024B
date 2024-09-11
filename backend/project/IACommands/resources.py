from flask_restful import Resource, reqparse
from flask import abort
from nltk import word_tokenize
from flask_jwt_extended import jwt_required
from Exceptions.CommandException import InvalidCommandError
from project.models import CommandModel
from project import db

class ProcesarComando(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('comando', type=str, help='Comando en lenguaje natural', required=True)

    @jwt_required()  # Asegura que solo usuarios autenticados puedan ejecutar comandos
    def post(self):
        try:
            args = self.parser.parse_args()
        except Exception as e:
            abort(400, description=str(e))

        comando = args['comando']
        try:
            # Aquí podemos agregar lógica de NLP para analizar el comando
            respuesta = self.analizar_comando(comando)
        except InvalidCommandError as e:
            abort(e.code, description=e.message + " " + e.message)

        # Devolver la respuesta al cliente
        return {'respuesta': respuesta}, 200

    def analizar_comando(self, comando):
        # Lógica básica para tokenizar el comando
        palabras = word_tokenize(comando.lower())

        # return 200, palabras

        # Aquí es donde podríamos agregar más lógica para mapear comandos a acciones reales
        if 'crear' in palabras and 'cuenta' in palabras:
            # Por ejemplo, si el comando es "crear una cuenta"
            return "Creando una cuenta para el usuario..."

        # Si no reconocemos el comando
        raise InvalidCommandError(comando)

# Excepción personalizada para comandos inválidos
class InvalidCommandError(Exception):
    def __init__(self, command):
        self.code = 400
        self.message = f'Comando inválido: {command}'
