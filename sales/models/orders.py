import uuid

from . import db, Worker


class Order(db.Model):
    """description of food model for SQLAlchemy """
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True)
    quantity = db.Column(db.Integer)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'))


    def __init__(self, worker, food, quantity):
        self.worker = worker
        self.food = food
        self.quantity = quantity
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f'Order ({self.worker}, {self.food},  {self.quantity}, {self.uuid} )'

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'worker': self.worker.to_dict(),
            'food': self.food.to_dict(),
            'quantity': self.quantity,
        }
