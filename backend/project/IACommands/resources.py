from flask_restful import Resource, reqparse
from flask import abort
from flask_jwt_extended import jwt_required
import spacy
from spacy.matcher import Matcher

class ProcesarComando(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('comando', type=str, help='Comando en lenguaje natural', required=True)
        self.nlp = spacy.load('es_core_news_sm')
        self.matcher = Matcher(self.nlp.vocab)
        self.configurar_patrones()

    def configurar_patrones(self):
        # Definir patrones como en el paso 2
        pattern_crear_cuenta = [
            {'LEMMA': 'crear'},
            {'LOWER': 'una', 'OP': '?'},
            {'LOWER': {'IN': ['cuenta', 'usuario']}}
        ]
        pattern_servidor = [
            {'LEMMA': 'servidor'},
            {'IS_ALPHA': True, 'OP': '+'}
        ]
        pattern_grupo = [
            {'LEMMA': 'grupo'},
            {'IS_ALPHA': True, 'OP': '+'}
        ]
        pattern_duracion = [
            {'LEMMA': 'duración'},
            {'LOWER': 'de', 'OP': '?'},
            {'IS_DIGIT': True},
            {'LOWER': {'IN': ['mes', 'meses', 'día', 'días', 'año', 'años']}}
        ]

        self.matcher.add('CREAR_CUENTA', [pattern_crear_cuenta])
        self.matcher.add('SERVIDOR', [pattern_servidor])
        self.matcher.add('GRUPO', [pattern_grupo])
        self.matcher.add('DURACION', [pattern_duracion])

    @jwt_required()
    def post(self):
        try:
            args = self.parser.parse_args()
            comando = args['comando']
            respuesta = self.analizar_comando(comando)
            return {'respuesta': respuesta}, 200
        except Exception as e:
            abort(400, description=str(e))

    def analizar_comando(self, comando):
        doc = self.nlp(comando.lower())
        matches = self.matcher(doc)

        datos = {
            'accion': None,
            'servidor': None,
            'grupo': None,
            'duracion': None,
            'informacion_faltante': []
        }

        for match_id, start, end in matches:
            span = doc[start:end]
            match_label = self.nlp.vocab.strings[match_id]

            if match_label == 'CREAR_CUENTA':
                datos['accion'] = 'crear_cuenta'
            elif match_label == 'SERVIDOR':
                datos['servidor'] = span.text.split()[-1]
            elif match_label == 'GRUPO':
                datos['grupo'] = span.text.split()[-1]
            elif match_label == 'DURACION':
                datos['duracion'] = ' '.join([token.text for token in span if token.like_num or token.pos_ == 'NOUN'])

        # Identificar información faltante
        for key in ['accion', 'servidor', 'grupo', 'duracion']:
            if not datos[key]:
                datos['informacion_faltante'].append(key)

        # Generar respuesta
        if datos['informacion_faltante']:
            respuesta_usuario = f"Necesito la siguiente información: {', '.join(datos['informacion_faltante'])}."
        else:
            respuesta_usuario = f"Entendido. Voy a {datos['accion']} para el servidor {datos['servidor']} en el grupo {datos['grupo']} con una duración de {datos['duracion']}."

        return respuesta_usuario
