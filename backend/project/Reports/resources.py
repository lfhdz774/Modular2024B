from flask_restful import Resource,reqparse,request
from flask import jsonify,abort
from project.models import Server
from project import db
from flasgger.utils import swag_from

class ChartReport(Resource):
    @swag_from('project/swagger.yaml') 
    def get(self):
        servers = Server.query.all()
        chart_data = []

        for server in servers:
            credentials_count = len(server.accesses)
            chart_data.append({
            'server_name': server.name,
            'credentials_count': credentials_count
            })

        return jsonify(chart_data)