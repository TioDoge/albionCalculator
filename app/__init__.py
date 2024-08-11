from flask import Flask
from flask_restful import Api
from .common.generate_response import generate_response

# importacion de extenciones
from .db import db
from .ext import marshmallow, migrate, cors
from .common.error_handling import *

# importacion de blueprints
from .routes.routes import routes_blueprint

def create_app(settings_module):
    app = Flask(__name__)
    app.config.from_object(settings_module)
    
    # Inicializa las extenciones
    db.init_app(app)
    marshmallow.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={ r'/api/*': { 'origins': ['http://localhost:3000'] } })
    
    # Captura todos los errores 404
    Api(app, catch_all_404s=True)
    
    # Registra los blueprints
    app.register_blueprint(routes_blueprint)
    
    return app

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception_error(e):
        return generate_response(message="Internal Server Error", status=500, data=e)
    
    @app.errorhandler(405)
    def handle_405_error(e):
        return generate_response(message="Method not allowed", status=405, data=e)
    
    @app.errorhandler(403)
    def handle_403_error(e):
        return generate_response(message="Forbidden error", status=403, data=e)
    
    @app.errorhandler(404)
    def handle_404_error(e):
        return generate_response(message="Not Found error", status=404, data=e)
    
    @app.errorhandler(AppErrorBaseClass)
    def handle_app_base_error(e):
        return generate_response(message=str(e), status=500)
    
    @app.errorhandler(ObjectNotFound)
    def handle_object_not_found_error(e):
        return generate_response(message=str(e), status=404)