import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
    )
_user_parser.add_argument('password',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
    )

class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "user already exists."}, 400 #Bad Request

        user = UserModel(**data)
        try:
            user.upsert_to_db()
        except:
            return {"message": "An error ocurred creating the user."}, 500 #Internal Server Error
        
        return {'message': 'user created succefully'}, 201 #Created


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'user not found'}, 404 #Not Found
        return user.json()
        

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'user not found'}, 404 #Not Found
        user.delete_from_db()
        return {'message': 'user deleted'}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if (user and user.password == data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'invalid credentials'}, 401
