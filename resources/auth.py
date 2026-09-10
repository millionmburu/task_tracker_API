
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from config import db
from models import User

#~~~~~~~~ Signup Class ~~~~~~~~#
class SignUp(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return{'error':'Both username and password are required'}, 422

        if User.query.filter_by(username=username).first():
            return{'error':'The username is already taken.'}, 422

        try:
            new_user = User(username=username)
            new_user.password_hash = password
            db.session.add(new_user)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            return{'error': str(e)}, 422

        access_token = create_access_token(identity=str(new_user.id))
        return{
            'user': new_user.to_dict(),
            'access_token': access_token
        }, 201

#~~~~~~~~ Login Class ~~~~~~~~#
class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not user.authenticate(password):
            return{'error':'Invalid username or password'}, 401

        access_token = create_access_token(identity=str(user.id))
        return{
            'user':user.to_dict(),
            'access_token': access_token
        }, 200

#~~~~~~~~ Me Class ~~~~~~~~#
class Me(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        if not user:
            return{'error': 'User not found'}, 404
        return user.to_dict(), 200
    


