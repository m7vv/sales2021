from flask import request
from flask_restful import Resource

from sales.models import db
from sales.models.orders import Order


class OrdersApi(Resource):

    def get(self, uuid=None):
        if not uuid:
            orders = db.session.query(Order).all()
            return [f.to_dict() for f in orders], 200
        order = db.session.query(Order).filter_by(uuid=uuid).first()
        if not order:
            return "", 404
        return order.to_dict(), 200

    def post(self):
        order_json = request.json
        if not order_json:
            return {'message': 'Wrong data'}, 400
        try:
            order = Order(
                name=order_json['name'],
                price=order_json.get('price'),
            )
            db.session.add(order)
            db.session.commit()
        except (ValueError, KeyError):
            return {'message': 'Wrong data'}, 400
        return {'message': 'Created successfully', 'uuid': order.uuid}, 201

    def put(self, uuid):
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
            return {'message': 'Wrong data'}, 400
        return {'message': 'Updated successfully'}, 200

    def patch(self, uuid):
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
        return {'message': 'Updated successfully'}, 200

    def delete(self, uuid):
        order = db.session.query(Order).filter_by(uuid=uuid).first()
        if not order:
            return "", 404
        db.session.delete(order)
        db.session.commit()
        return '', 204
