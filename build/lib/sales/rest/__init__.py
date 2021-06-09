from flask_restful import Api

from .orders import OrdersApi
from .foods import FoodsApi
from .workers import WorkersApi


def init_app(app):
    api = Api(app)
    api.add_resource(FoodsApi, '/api/foods', '/api/foods/<uuid>', strict_slashes=False)
    api.add_resource(WorkersApi, '/api/workers', '/api/workers/<uuid>', strict_slashes=False)
    api.add_resource(OrdersApi, '/api/orders', '/api/orders/<uuid>', strict_slashes=False)
