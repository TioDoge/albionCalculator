from flask import Blueprint
from flask_restful import Api
from ..views.albion_view import *

routes_blueprint = Blueprint("routes", __name__, url_prefix='/api')
api = Api(routes_blueprint)

api.add_resource(obtenerValoresCraft, '/gastos')