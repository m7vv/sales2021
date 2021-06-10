import uuid

from . import db, Worker


class Order(db.Model):
    """description of food model for SQLAlchemy """
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True)
    quantity = db.Column(db.Integer)
    worker = db.Column(db.Integer, db.ForeignKey('worker.id'))
    food = db.Column(db.Integer, db.ForeignKey('food.id'))

    def __init__(self, worker, food, quantity):
        self.worker = worker
        self.food = food
        self.quantity = quantity
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f'Order ({self.worker}, {self.food},  {self.quantity}, {self.uuid} )'

    def to_dict(self):
        return {
            'worker': self.worker,
            'uuid': self.uuid,
            'quantity': self.quantity,
            'food': self.food,

        }
