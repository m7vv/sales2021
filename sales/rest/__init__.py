from flask_restful import Api

from .orders import OrdersApi
from .smoke import Smoke
from .films import FilmListApi
from .foods import FoodsApi
from .workers import WorkersApi


def init_app(app):
    api = Api(app)
    api.add_resource(Smoke, '/m')
    api.add_resource(FilmListApi, '/films', '/films/<uuid>', strict_slashes=False)
    api.add_resource(FoodsApi, '/foods', '/foods/<uuid>', strict_slashes=False)
    api.add_resource(WorkersApi, '/workers', '/workers/<uuid>', strict_slashes=False)
    api.add_resource(OrdersApi, '/orders', '/orders/<uuid>', strict_slashes=False)
