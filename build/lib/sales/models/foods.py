import uuid

from . import db


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    uuid = db.Column(db.String(36), unique=True)
    price = db.Column(db.Integer)
    orders = db.relationship('Order', backref='food_orders')

    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f'Food ({self.name}, {self.price}, {self.uuid} )'

    def to_dict(self):
        return {
            'name': self.name,
            'uuid': self.uuid,
            'price': self.price
        }
