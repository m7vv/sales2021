from flask_restful import Api
from .smoke import Smoke
from .films import FilmListApi


def init_app(app):
    api = Api(app)
    api.add_resource(Smoke, '/m')
    api.add_resource(FilmListApi, '/films', '/films/<uuid>', strict_slashes=False)
