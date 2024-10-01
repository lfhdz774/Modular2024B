from flask import Blueprint
from flask_restful import Resource
from flask_restful import Api,Resource

from project import app
from .resources import ChartReport
reports_blueprint = Blueprint('ReportService', __name__, url_prefix='/api/admin')
api = Api(reports_blueprint)

api.add_resource(ChartReport, '/report/AccessesCount')