import uuid

from . import db


class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True)
    name = db.Column(db.String, nullable=False)
    salary = db.Column(db.Integer)
    orders = db.relationship('Order', backref='worker_orders')

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f'Worker ({self.name}, {self.salary}, {self.uuid} )'

    def to_dict(self):
        return {
            'name': self.name,
            'uuid': self.uuid,
            'salary': self.salary
        }
