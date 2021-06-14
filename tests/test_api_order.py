import tempfile
import unittest

from sales import create_app
from sales.models import Food, Worker, Order

base_order_url = '/api/orders/'


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
        response = TestOrderApi.app.test_client().get(f'{base_order_url}')
        self.assertEqual(3, len(response.json))
        self.assertIn("'quantity': 1", str(response.json))

    def test_get_order_by_uuid(self):
        with TestOrderApi.app.app_context():
            from sales.models import db
            order = db.session.query(Order).filter_by(quantity=2).first()
        response = TestOrderApi.app.test_client().get(f'{base_order_url}{order.uuid}')
        self.assertEqual("Ivanov", response.json["worker"]["name"])

    def test_get_order_by_uuid_wrong(self):
        response = TestOrderApi.app.test_client().get(f'{base_order_url}56')
        self.assertEqual(404, response.status_code)

    def test_post_order_with_empty_json(self):
        response = TestOrderApi.app.test_client().post(f'{base_order_url}')
        self.assertEqual('Wrong data', response.json['message'])

    def test_post_order_ok(self):
        with TestOrderApi.app.app_context():
            from sales.models import db
            worker = db.session.query(Worker).first()
            food = db.session.query(Food).first()
        new_order = dict(worker_uuid=worker.uuid, food_uuid=food.uuid, quantity=12)
        response = TestOrderApi.app.test_client().post(f'{base_order_url}', json=new_order)
        self.assertEqual('Created successfully', response.json['message'])
        response = TestOrderApi.app.test_client().get(f'{base_order_url}')
        self.assertEqual(4, len(response.json))

    def test_post_order_wrong_data(self):
        with TestOrderApi.app.app_context():
            from sales.models import db
            worker = db.session.query(Worker).first()
            food = db.session.query(Food).first()
        new_order = dict(worker_uuid=worker.uuid, food_uuid=food.uuid, numbers=2)
        response = TestOrderApi.app.test_client().post(f'{base_order_url}', json=new_order)
        self.assertEqual('Wrong data', response.json['message'])

    def test_put_order_ok(self):
        with TestOrderApi.app.app_context():
            from sales.models import db
            order = db.session.query(Order).first()
            worker = db.session.query(Worker).first()
            food = db.session.query(Food).first()
        new_order = dict(worker_uuid=worker.uuid, food_uuid=food.uuid, quantity=80)
        response = TestOrderApi.app.test_client().put(f'{base_order_url}{order.uuid}', json=new_order)
        self.assertEqual('Updated successfully', response.json['message'])
        response = TestOrderApi.app.test_client().get(f'{base_order_url}')
        self.assertEqual(3, len(response.json))
        response = TestOrderApi.app.test_client().get(f'{base_order_url}{order.uuid}')
        self.assertEqual(80, response.json['quantity'])

    def test_put_order_good_uuid_wrong_data(self):
        with TestOrderApi.app.app_context():
            from sales.models import db
            order = db.session.query(Order).first()
            worker = db.session.query(Worker).first()
            food = db.session.query(Food).first()
        new_order = dict(worker_uuid=worker.uuid, food_uuid=food.uuid, fake=80)
        response = TestOrderApi.app.test_client().put(f'{base_order_url}{order.uuid}', json=new_order)
        self.assertEqual('Wrong data', response.json['message'])
        response = TestOrderApi.app.test_client().get(f'{base_order_url}')
        self.assertEqual(3, len(response.json))
        response = TestOrderApi.app.test_client().get(f'{base_order_url}{order.uuid}')
        self.assertEqual(2, response.json['quantity'])

    def test_delete_order_by_uuid(self):
        with TestOrderApi.app.app_context():
            from sales.models import db
            order = db.session.query(Order).first()
        response = TestOrderApi.app.test_client().delete(f'{base_order_url}{order.uuid}')
        self.assertEqual(204, response.status_code)
        response = TestOrderApi.app.test_client().get(f'{base_order_url}')
        self.assertEqual(2, len(response.json))


    def test_delete_order_by_uuid_wrong(self):
        response = TestOrderApi.app.test_client().delete(f'{base_order_url}255')
        self.assertEqual(404, response.status_code)


