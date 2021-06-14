import tempfile
import unittest

from sales import create_app
from sales.models.workers import Worker


class TestWorkerApi(unittest.TestCase):
    """test cases for worker api"""
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

        with TestWorkerApi.app.app_context():
            from sales.models import db
            db.create_all()
            db.session.add(ivanov)
            db.session.add(petrov)
            db.session.add(nazarov)
            db.session.commit()
            db.session.close()

    def tearDown(self):
        with TestWorkerApi.app.app_context():
            from sales.models import db
            db.session.remove()
            db.drop_all()

    def test_get_all_workers(self):
        response = TestWorkerApi.app.test_client().get('/api/workers')
        self.assertIn(b'"name": "Nazarov"', response.data)

    def test_get_worker_by_uuid(self):
        with TestWorkerApi.app.app_context():
            from sales.models import db
            worker = db.session.query(Worker).filter_by(name='Petrov').first()
        response = TestWorkerApi.app.test_client().get(f'/api/workers/{worker.uuid}')
        self.assertIn(b'"salary": 7000', response.data)

    def test_get_worker_by_uuid_wrong(self):
        response = TestWorkerApi.app.test_client().get(f'/api/workers/777')
        self.assertEqual(404, response.status_code)

    def test_post_worker_with_empty_json(self):
        response = TestWorkerApi.app.test_client().post('/api/workers')
        self.assertEqual('Wrong data', response.json['message'])

    def test_post_worker_ok(self):
        new_worker = dict(name='Lomov', salary=3400)
        response = TestWorkerApi.app.test_client().post('/api/workers', json=new_worker)
        self.assertEqual('Created successfully', response.json['message'])

    def test_post_worker_good_uuid_wrong_data(self):
        new_worker = dict(surname='Mosha', love=3040)
        response = TestWorkerApi.app.test_client().post('/api/workers', json=new_worker)
        self.assertEqual('Wrong data', response.json['message'])

    def test_put_worker_wrong(self):
        response = TestWorkerApi.app.test_client().put('/api/workers/23')
        self.assertEqual(400, response.status_code)

    def test_put_worker_good(self):
        with TestWorkerApi.app.app_context():
            from sales.models import db
            worker = db.session.query(Worker).filter_by(name='Nazarov').first()
        new_worker = dict(name='Mirash', salary=7412)
        response = TestWorkerApi.app.test_client().put(f'/api/workers/{worker.uuid}', json=new_worker)
        self.assertEqual(200, response.status_code)

    def test_put_worker_good_uuid_wrong_data(self):
        with TestWorkerApi.app.app_context():
            from sales.models import db
            worker = db.session.query(Worker).filter_by(name='Nazarov').first()
        new_worker = dict(price="Never")
        response = TestWorkerApi.app.test_client().put(f'/api/workers/{worker.uuid}', json=new_worker)
        self.assertEqual(400, response.status_code)

    def test_patch_worker_uuid_wrong(self):
        response = TestWorkerApi.app.test_client().patch('/api/workers/899')
        self.assertEqual(404, response.status_code)

    def test_patch_worker_good_salary(self):
        with TestWorkerApi.app.app_context():
            from sales.models import db
            worker = db.session.query(Worker).filter_by(name='Ivanov').first()
        new_worker = dict(salary=8900)
        response = TestWorkerApi.app.test_client().patch(f'/api/workers/{worker.uuid}', json=new_worker)
        self.assertEqual(200, response.status_code)

    def test_patch_worker_good_name(self):
        with TestWorkerApi.app.app_context():
            from sales.models import db
            worker = db.session.query(Worker).filter_by(name='Ivanov').first()
        new_worker = dict(name="Ivanov Jr")
        response = TestWorkerApi.app.test_client().patch(f'/api/workers/{worker.uuid}', json=new_worker)
        self.assertEqual(200, response.status_code)

    def test_patch_worker_good_uuid_wrong_data(self):
        with TestWorkerApi.app.app_context():
            from sales.models import db
            worker = db.session.query(Worker).filter_by(name='Nazarov').first()
        new_worker = dict(sal="boo")
        response = TestWorkerApi.app.test_client().patch(f'/api/workers/{worker.uuid}', json=new_worker)
        self.assertEqual(200, response.status_code)

    def test_delete_worker_by_uuid(self):
        with TestWorkerApi.app.app_context():
            from sales.models import db
            worker = db.session.query(Worker).filter_by(name='Nazarov').first()
        response = TestWorkerApi.app.test_client().delete(f'/api/workers/{worker.uuid}')

        response = TestWorkerApi.app.test_client().get(f'/api/workers/{worker.uuid}')
        self.assertNotIn(b'"salary": 5500', response.data)

    def test_delete_worker_by_uuid_wrong(self):
        response = TestWorkerApi.app.test_client().delete(f'/api/workers/255')
        self.assertEqual(404, response.status_code)




if __name__ == '__main__':
    unittest.main()
