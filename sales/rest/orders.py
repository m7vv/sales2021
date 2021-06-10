import logging


from flask import request
from flask_restful import Resource

from sales.models import db
from sales.models.orders import Order


class OrdersApi(Resource):
    """
    A class to specify api for orders items

    Methods
    ______
    get(self, uuid=None)
    post(self)
    put(self, uuid)
    patch(self, uuid)
    delete(self, uuid)
    """

    def get(self, uuid=None):
        """return all orders in JSON format if uuid=None otherwise return specific order specified by uuid"""
        if not uuid:
            orders = db.session.query(Order).all()
            return [f.to_dict() for f in orders], 200
        order = db.session.query(Order).filter_by(uuid=uuid).first()
        if not order:
            return "", 404
        return order.to_dict(), 200

    def post(self):
        """create new order item based on request JSON data"""
        order_json = request.json
        if not order_json:
            logging.error('Attempt to create  order without json')
            return {'message': 'Wrong data'}, 400
        try:
            order = Order(
                name=order_json['name'],
                price=order_json.get('price'),
            )
            db.session.add(order)
            db.session.commit()
        except (ValueError, KeyError):
            logging.error(f'Order was not created due wrong data')
            return {'message': 'Wrong data'}, 400
        logging.info(f'Order with uuid {order.uuid} was created')
        return {'message': 'Created successfully', 'uuid': order.uuid}, 201

    def put(self, uuid):
        """update whole order item specified by uuid based on request JSON data"""
        order_json = request.json
        if not order_json:
            return {'message': 'Wrong data'}, 400
        try:
            db.session.query(Order).filter_by(uuid=uuid).update(
                dict(
                    name=order_json['name'],
                    price=order_json.get('price')
                )
            )
            db.session.commit()
        except (ValueError, KeyError):
            logging.error(f'Order with uuid {uuid} was not updated due wrong data')
            return {'message': 'Wrong data'}, 400
        logging.info(f'Order with uuid {uuid} was updated')
        return {'message': 'Updated successfully'}, 200

    def patch(self, uuid):
        """update parts of order item specified by uuid based on request JSON data"""
        order = db.session.query(Order).filter_by(uuid=uuid).first()
        if not order:
            return "", 404
        order_json = request.json
        name = order_json.get('name')
        price = order_json.get('price')

        if name:
            order.name = name
        elif price:
            order.price = price

        db.session.add(order)
        db.session.commit()
        logging.info(f'Order with uuid {uuid} was updated')
        return {'message': 'Updated successfully'}, 200

    def delete(self, uuid):
        """delete worker item specified by uuid"""
        order = db.session.query(Order).filter_by(uuid=uuid).first()
        if not order:
            return "", 404
        db.session.delete(order)
        db.session.commit()
        logging.info(f'Order with uuid {uuid} was deleted')
        return '', 204
