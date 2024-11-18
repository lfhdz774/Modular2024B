from flask_jwt_extended import decode_token, get_jwt_identity, verify_jwt_in_request
from flask import request, jsonify
from flask_restful import Resource
import jwt
from flask_cors import cross_origin

class PasswordView(Resource):

    def get(self, token):
        try:
            if request.method == 'OPTIONS':
                return {'message': 'success'}, 204
            # Decodificar el token para obtener el payload
            decoded_token = decode_token(token)
            print('Token decodificado:', decoded_token)
            # Obtener la contraseña del payload
            password = decoded_token['user_claims']['password']

            return {'password': password}, 200

        except Exception as e:
            print('Error al decodificar el token:', e)
            return {'message': 'Enlace inválido. ' + str(e)}, 404