from flask import request
from flask_restful import Resource

from sales.models import db
from sales.models.foods import Food


class FoodsApi(Resource):

    def get(self, uuid=None):
        if not uuid:
            foods = db.session.query(Food).all()
            return [f.to_dict() for f in foods], 200
        food = db.session.query(Food).filter_by(uuid=uuid).first()
        if not food:
            return "", 404
        return food.to_dict(), 200

    def post(self):
        food_json = request.json
        if not food_json:
            return {'message': 'Wrong data'}, 400
        try:
            food = Food(
                name=food_json['name'],
                price=food_json.get('price'),
            )
            db.session.add(food)
            db.session.commit()
        except (ValueError, KeyError):
            return {'message': 'Wrong data'}, 400
        return {'message': 'Created successfully', 'uuid': food.uuid}, 201

    def put(self, uuid):
        food_json = request.json
        if not food_json:
            return {'message': 'Wrong data'}, 400
        try:
            db.session.query(Food).filter_by(uuid=uuid).update(
                dict(
                    name=food_json['name'],
                    price=food_json.get('price')
                )
            )
            db.session.commit()
        except (ValueError, KeyError):
            return {'message': 'Wrong data'}, 400
        return {'message': 'Updated successfully'}, 200

    def patch(self, uuid):
        food = db.session.query(Food).filter_by(uuid=uuid).first()
        if not food:
            return "", 404
        food_json = request.json
        name = food_json.get('name')
        price = food_json.get('price')

        if name:
            food.name = name
        elif price:
            food.price = price

        db.session.add(food)
        db.session.commit()
        return {'message': 'Updated successfully'}, 200

    def delete(self, uuid):
        food = db.session.query(Food).filter_by(uuid=uuid).first()
        if not food:
            return "", 404
        db.session.delete(food)
        db.session.commit()
        return '', 204
