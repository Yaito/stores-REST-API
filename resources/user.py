import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
            type=str,
            required=True,
            help="This field cannot be blank."
        )
    parser.add_argument('password',
            type=str,
            required=True,
            help="This field cannot be blank."
        )

    def post(self):
        data = UserRegister.parser.parse_args()

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
        user = UserModel.find_by_username(user_id)
        if not user:
            return {'message': 'user not found'}, 404 #Not Found
        return user.json
        

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'user not found'}, 404 #Not Found
        user.delete_from_db()
        return {'message': 'user deleted'}, 200