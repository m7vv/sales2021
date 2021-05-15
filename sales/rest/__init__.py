from flask_restful import Api
from .smoke import Smoke


def init_app(app):
    api = Api(app)

    api.add_resource(Smoke, '/m')
