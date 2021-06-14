import tempfile
import unittest

from sales import create_app
from sales.models import Food, Worker, Order


class TestOrderApi(unittest.TestCase):
    """test cases for ordder api"""
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_DATABASE_URI': "sqlite:///:memory:",
    })

    def setUp(self):
        ivanov = Worker(
            name='Ivanov',
            salary=6000,
        )
        petrov = Worker(
            name='Petrov',
            salary=7000,
        )
        nazarov = Worker(
            name='Nazarov',
            salary=5500,
        )
        hamburger = Food(
            name='Hamburger',
            price=2000,
        )
        pancake_milk = Food(
            name='Pancake with milk',
            price=1000,
        )
        order1 = Order(
            worker=ivanov,
            food=hamburger,
            quantity=2
        )
        order2 = Order(
            worker=nazarov,
            food=hamburger,
            quantity=3
        )
        order3 = Order(
            worker=ivanov,
            food=pancake_milk,
            quantity=1
        )

        with TestOrderApi.app.app_context():
            from sales.models import db
            db.create_all()
            db.session.add(ivanov)
            db.session.add(petrov)
            db.session.add(nazarov)
            db.session.add(hamburger)
            db.session.add(pancake_milk)
            db.session.add(order1)
            db.session.add(order2)
            db.session.add(order3)

            db.session.commit()
            db.session.close()

    def tearDown(self):
        with TestOrderApi.app.app_context():
            from sales.models import db
            db.session.remove()
            db.drop_all()

    def test_get_orders(self):
        response = TestOrderApi.app.test_client().get('/api/orders')
        print(response.json)
        self.assertIn(b'"name": "Hamburger"', response.data)