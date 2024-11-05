from flask_restful import Resource,reqparse,request
from flask import jsonify,abort
from project.models import Server, Access
from project import db
from flasgger.utils import swag_from

class ChartReport(Resource):
    @swag_from('project/swagger.yaml') 
    def get(self):
        servers = Server.query.all()
        chart_data = []

        for server in servers:
            credentials_count = len(server.access)
            chart_data.append({
            'server_name': server.name,
            'credentials_count': credentials_count
            })

        return jsonify(chart_data)

class ReportGenerator(Resource):
    @swag_from('project/swagger.yaml') 
    def post(self):
        # Parseamos los parámetros recibidos en la solicitud POST.
        parser = reqparse.RequestParser()
        parser.add_argument('idReporte', type=int, required=True, help='ID del reporte es obligatorio.')
        parser.add_argument('filtros', type=dict, required=True, help='Filtros del reporte son obligatorios.')
        args = parser.parse_args()

        id_reporte = args['idReporte']
        filtros = args['filtros']

        # Ejecutamos diferentes consultas según el ID del reporte.
        if id_reporte == 1:
            # Reporte de Acesos
            query = db.session.query(Access)
            
            # Aplicamos filtros opcionales
            if 'fechaInicio' in filtros and 'fechaFinal' in filtros:
                query = query.filter(Access.created_at.between(filtros['fechaInicio'], filtros['fechaFinal']))

            accesos = query.all()
            report_data = [{'id': acceso.access_id, 'Usuario': acceso.user.username, 'Expira el': acceso.expires_at} for acceso in accesos]

        elif id_reporte == 2:
            # Reporte de Inventario
            query = db.session.query(Inventory)

            if 'categoria' in filtros:
                query = query.filter(Inventory.category == filtros['categoria'])
            if 'cantidadMinima' in filtros:
                query = query.filter(Inventory.quantity >= filtros['cantidadMinima'])

            inventario = query.all()
            report_data = [{'id': item.id, 'nombre': item.name, 'cantidad': item.quantity} for item in inventario]

        else:
            abort(400, description='ID de reporte no válido.')

        return jsonify(report_data)