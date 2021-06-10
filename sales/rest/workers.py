import logging

from flask import request
from flask_restful import Resource

from sales.models import db
from sales.models.workers import Worker


class WorkersApi(Resource):
    """
    A class to specify api for workers items

    Methods
    ______
    get(self, uuid=None)
    post(self)
    put(self, uuid)
    patch(self, uuid)
    delete(self, uuid)
    """

    def get(self, uuid=None):
        """return all workers in JSON format if uuid=None otherwise retrun specific worker specified by uuid"""
        if not uuid:
            workers = db.session.query(Worker).all()
            return [f.to_dict() for f in workers], 200
        worker = db.session.query(Worker).filter_by(uuid=uuid).first()
        if not worker:
            return "", 404
        return worker.to_dict(), 200

    def post(self):
        """create new worker item based on request JSON data"""
        worker_json = request.json
        if not worker_json:
            logging.error('Attempt to create  worker without json')
            return {'message': 'Wrong data'}, 400
        try:
            worker = Worker(
                name=worker_json['name'],
                salary=worker_json.get('salary'),
            )
            db.session.add(worker)
            db.session.commit()
        except (ValueError, KeyError):
            logging.error(f'Worker was not created due wrong data')
            return {'message': 'Wrong data'}, 400
        logging.info(f'Worker with uuid {worker.uuid} was created')
        return {'message': 'Created successfully', 'uuid': worker.uuid}, 201

    def put(self, uuid):
        """update whole worker item specified by uuid based on request JSON data"""
        worker_json = request.json
        if not worker_json:
            return {'message': 'Wrong data'}, 400
        try:
            db.session.query(Worker).filter_by(uuid=uuid).update(
                dict(
                    name=worker_json['name'],
                    salary=worker_json.get('salary')
                )
            )
            db.session.commit()
        except (ValueError, KeyError):
            logging.error(f'Worker with uuid {uuid} was not updated due wrong data')
            return {'message': 'Wrong data'}, 400
        logging.info(f'Worker with uuid {uuid} was updated')
        return {'message': 'Updated successfully'}, 200

    def patch(self, uuid):
        """update parts of worker item specified by uuid based on request JSON data"""
        worker = db.session.query(Worker).filter_by(uuid=uuid).first()
        if not worker:
            return "", 404
        worker_json = request.json
        name = worker_json.get('name')
        salary = worker_json.get('salary')

        if name:
            worker.name = name
        elif salary:
            worker.salary = salary

        db.session.add(worker)
        db.session.commit()
        logging.info(f'Worker with uuid {uuid} was updated')
        return {'message': 'Updated successfully'}, 200

    def delete(self, uuid):
        """delete worker item specified by uuid"""
        worker = db.session.query(Worker).filter_by(uuid=uuid).first()
        if not worker:
            return "", 404
        db.session.delete(worker)
        db.session.commit()
        logging.info(f'Worker with uuid {uuid} was deleted')
        return '', 204
