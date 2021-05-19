from flask import request
from flask_restful import Resource

from sales.models import db
from sales.models.workers import Worker


class WorkersApi(Resource):

    def get(self, uuid=None):
        if not uuid:
            workers = db.session.query(Worker).all()
            return [f.to_dict() for f in workers], 200
        worker = db.session.query(Worker).filter_by(uuid=uuid).first()
        if not worker:
            return "", 404
        return worker.to_dict(), 200

    def post(self):
        worker_json = request.json
        if not worker_json:
            return {'message': 'Wrong data'}, 400
        try:
            worker = Worker(
                name=worker_json['name'],
                salary=worker_json.get('salary'),
            )
            db.session.add(worker)
            db.session.commit()
        except (ValueError, KeyError):
            return {'message': 'Wrong data'}, 400
        return {'message': 'Created successfully', 'uuid': worker.uuid}, 201

    def put(self, uuid):
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
            return {'message': 'Wrong data'}, 400
        return {'message': 'Updated successfully'}, 200

    def patch(self, uuid):
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
        return {'message': 'Updated successfully'}, 200

    def delete(self, uuid):
        worker = db.session.query(Worker).filter_by(uuid=uuid).first()
        if not worker:
            return "", 404
        db.session.delete(worker)
        db.session.commit()
        return '', 204
