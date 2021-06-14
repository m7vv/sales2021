import tempfile
import unittest

from sales import create_app
from sales.models.foods import Food


class TestFoodApi(unittest.TestCase):
    """test cases for order api"""
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_DATABASE_URI': "sqlite:///:memory:",
    })

    def setUp(self):
        hamburger = Food(
            name='Hamburger',
            price=2000,
        )
        pancake_milk = Food(
            name='Pancake with milk',
            price=1000,
        )
        with TestFoodApi.app.app_context():
            from sales.models import db
            db.create_all()
            db.session.add(hamburger)
            db.session.add(pancake_milk)
            db.session.commit()
            db.session.close()

    def tearDown(self):
        with TestFoodApi.app.app_context():
            from sales.models import db
            db.session.remove()
            db.drop_all()

    def test_get_food(self):
        response = TestFoodApi.app.test_client().get('/api/foods')
        self.assertIn(b'"name": "Hamburger"', response.data)

    def test_get_food_by_uuid(self):
        with TestFoodApi.app.app_context():
            from sales.models import db
            food = db.session.query(Food).filter_by(name='Pancake with milk').first()
        response = TestFoodApi.app.test_client().get(f'/api/foods/{food.uuid}')
        self.assertIn(b'"price": 1000', response.data)

    def test_post_food_wrong(self):
        response = TestFoodApi.app.test_client().post('/api/foods')
        self.assertEqual(b'{"message": "Wrong data"}\n', response.data)

    def test_post_food_ok(self):
        new_food = dict(name='Cake', price=340)
        response = TestFoodApi.app.test_client().post('/api/foods', json=new_food)
        self.assertEqual('Created successfully', response.json['message'])

    def test_post_food_good_uuid_wrong_data(self):
        new_food = dict(surname='Cake', money=340)
        response = TestFoodApi.app.test_client().post('/api/foods', json=new_food)
        self.assertEqual('Wrong data', response.json['message'])

    def test_put_food_wrong(self):
        response = TestFoodApi.app.test_client().put('/api/foods/67')
        self.assertEqual(400, response.status_code)

    def test_put_food_good(self):
        with TestFoodApi.app.app_context():
            from sales.models import db
            food = db.session.query(Food).filter_by(name='Pancake with milk').first()
        new_food = dict(name='Cake', price=340)
        response = TestFoodApi.app.test_client().put(f'/api/foods/{food.uuid}', json=new_food)
        self.assertEqual(200, response.status_code)

    def test_put_food_good_uuid_wrong_data(self):
        with TestFoodApi.app.app_context():
            from sales.models import db
            food = db.session.query(Food).filter_by(name='Pancake with milk').first()
        new_food = dict(sal="Big Cake")
        response = TestFoodApi.app.test_client().put(f'/api/foods/{food.uuid}', json=new_food)
        self.assertEqual(400, response.status_code)

    def test_patch_food_wrong(self):
        response = TestFoodApi.app.test_client().patch('/api/foods/67')
        self.assertEqual(404, response.status_code)

    def test_patch_food_good_price(self):
        with TestFoodApi.app.app_context():
            from sales.models import db
            food = db.session.query(Food).filter_by(name='Pancake with milk').first()
        new_food = dict(price=500)
        response = TestFoodApi.app.test_client().patch(f'/api/foods/{food.uuid}', json=new_food)
        self.assertEqual(200, response.status_code)

    def test_patch_food_good_name(self):
        with TestFoodApi.app.app_context():
            from sales.models import db
            food = db.session.query(Food).filter_by(name='Pancake with milk').first()
        new_food = dict(name="Big Cake")
        response = TestFoodApi.app.test_client().patch(f'/api/foods/{food.uuid}', json=new_food)
        self.assertEqual(200, response.status_code)

    def test_patch_food_good_uuid_wrong_data(self):
        with TestFoodApi.app.app_context():
            from sales.models import db
            food = db.session.query(Food).filter_by(name='Pancake with milk').first()
        new_food = dict(sal="Big Cake")
        response = TestFoodApi.app.test_client().patch(f'/api/foods/{food.uuid}', json=new_food)
        self.assertEqual(200, response.status_code)

    def test_delete_food_by_uuid(self):
        with TestFoodApi.app.app_context():
            from sales.models import db
            food = db.session.query(Food).filter_by(name='Pancake with milk').first()
        TestFoodApi.app.test_client().delete(f'/api/foods/{food.uuid}')
        response = TestFoodApi.app.test_client().get(f'/api/foods/{food.uuid}')
        self.assertNotIn(b'"price": 1000', response.data)


if __name__ == '__main__':
    unittest.main()
