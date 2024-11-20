from flask_restful import Resource,reqparse,request
from flask import jsonify,abort
from project.models import Server, Access,UserModel,Group
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
            report_data = [{'id': acceso.access_id, 'Acceso': acceso.access_name, 'Servidor': acceso.server.name,'Servidor Hostname': acceso.server.hostname, 'Usuario': acceso.user.username } for acceso in accesos]

        elif id_reporte == 2:
            # Reporte de Inventario
            query = db.session.query(Server)
            # Aplicamos filtros opcionales
            if 'fechaInicio' in filtros and 'fechaFinal' in filtros:
                query = query.filter(Server.created_at.between(filtros['fechaInicio'], filtros['fechaFinal']))
            servers = query.all()
            report_data = [{'id': server.server_id,'Shortname': server.short_name,'Hostname': server.hostname,'IP_Address': server.ip_address,'server_name': server.name} for server in servers]
        elif id_reporte == 3:
            # Reporte de Inventario
            query = db.session.query(UserModel)
            # Aplicamos filtros opcionales
            if 'fechaInicio' in filtros and 'fechaFinal' in filtros:
                query = query.filter(UserModel.created_at.between(filtros['fechaInicio'], filtros['fechaFinal']))
            users = query.all()
            report_data = [{'id': user.user_id,'Cuenta': user.username,'Email': user.email,'Codigo de Empleado': user.employee_code,'Nombre': user.first_name + ' '+ user.last_name} for user in users]
        elif id_reporte == 4:
            # Reporte de Inventario
            query = db.session.query(Group)
            # Aplicamos filtros opcionales
            if 'fechaInicio' in filtros and 'fechaFinal' in filtros:
                query = query.filter(Group.created_at.between(filtros['fechaInicio'], filtros['fechaFinal']))
            groups = query.all()
            report_data = [{'id': group.group_id,'Group Name': group.group_name,'Descripcion': group.description,'Servidor ID': group.server_id} for group in groups]
        else:
            abort(400, description='ID de reporte no válido.')

        return jsonify(report_data)