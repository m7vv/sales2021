import logging

from flask import request
from flask_restful import Resource

from sales.models import db
from sales.models.foods import Food


class FoodsApi(Resource):
    """
    A class to specify api for foods items

    Methods
    ______
    get(self, uuid=None)
    post(self)
    put(self, uuid)
    patch(self, uuid)
    delete(self, uuid)
    """

    def get(self, uuid=None):
        """returns all foods in JSON format if uuid=None otherwise retrun specific food specified by uuid"""
        if not uuid:
            foods = db.session.query(Food).all()
            return [f.to_dict() for f in foods], 200
        food = db.session.query(Food).filter_by(uuid=uuid).first()
        if not food:
            return "", 404
        return food.to_dict(), 200

    def post(self):
        """create new food item based on request JSON data"""
        food_json = request.json
        if not food_json:
            logging.error('Attempt to create  food without json')
            return {'message': 'Wrong data'}, 400
        try:
            food = Food(
                name=food_json['name'],
                price=food_json.get('price'),
            )
            db.session.add(food)
            db.session.commit()
        except (ValueError, KeyError):
            logging.error(f'Food was not created due wrong data')
            return {'message': 'Wrong data'}, 400
        logging.info(f'Food with uuid {food.uuid} was created')
        return {'message': 'Created successfully', 'uuid': food.uuid}, 201

    def put(self, uuid):
        """update whole food item specified by uuid based on request JSON data"""
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
            logging.error(f'Food with uuid {uuid} was not updated due wrong data')
            return {'message': 'Wrong data'}, 400
        logging.info(f'Food with uuid {uuid} was updated')
        return {'message': 'Updated successfully'}, 200

    def patch(self, uuid):
        """update parts of patch item specified by uuid based on request JSON data"""
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
        logging.info(f'Food with uuid {uuid} was updated')
        return {'message': 'Updated successfully'}, 200

    def delete(self, uuid):
        """delete food item specified by uuid"""
        food = db.session.query(Food).filter_by(uuid=uuid).first()
        if not food:
            return "", 404
        db.session.delete(food)
        db.session.commit()
        logging.info(f'Food with uuid {uuid} was deleted')
        return '', 204
