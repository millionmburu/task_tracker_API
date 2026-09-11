
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from config import db
from models import Task

#~~~~~~~~ TaskList Class ~~~~~~~~
class TaskList(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())

        #The pagination using query params
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        #filter to refute another user seeing the tasks of another 
        pagination = Task.query.filter_by(user_id=user_id).paginate(
            page=page, per_page=per_page,error_out=False
        )

        return{
            'tasks': [task.to_dict() for task in pagination.items],
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages,
            'per_page': pagination.per_page
        }, 200

    @jwt_required()
    def post(self):
        user_id = int(get_jwt_identity())
        data= request.get_json()

        try:
            new_task = Task(
                title= data.get('title'),
                description= data.get('description'),
                completed= data.get('completed', False),
                user_id=user_id #Acquired from the token 
            )
            db.session.add(new_task)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            return {'error': str(e)}, 422

        return new_task.to_dict(), 201

#~~~~~~~~ TaskList Class ~~~~~~~~
class TaskDetail(Resource):
    def _get_owned_task_or_none(self, task_id, user_id):
        #Fetches a task only if it belongs to the user
        return Task.query.filter_by(id=task_id, user_id=user_id).first()

    @jwt_required()
    def patch(self, task_id):
        user_id = int(get_jwt_identity())
        task = self._get_owned_task_or_none(task_id, user_id)

        if not task:
            #404 error not found
            return{'error': 'Task not found!'}, 404

        data = request.get_json()
        try:
            if 'title' in data:
                task.title = data['title']
            if 'description' in data:
                task.description = data['description']
            if 'completed' in data:
                task.completed = data['completed']
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            return{'error': str(e)}, 422

        return task.to_dict(), 200

    @jwt_required()
    def delete(self, task_id):
        user_id = int(get_jwt_identity())
        task = self._get_owned_task_or_none(task_id, user_id)

        if not task:
            return{'error': 'Task not found!'}, 404

        db.session.delete(task)
        db.session.commit()
        return{}, 204