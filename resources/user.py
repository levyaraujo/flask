from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp

atributes = reqparse.RequestParser()
atributes.add_argument('login', type=str, required=True)
atributes.add_argument('password', type=str, required=True)


class User(Resource):
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': f'User id {user_id} not found'}, 404

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                {
                    'message':
                    f'An internal error ocurred trying to delete {user_id}'
                }, 500
            return {'message': f'{user_id} was deleted.'}

        return f'{user_id} not found.', 404


class UserRegister(Resource):
    def post(self):
        data = atributes.parse_args()

        if UserModel.find_login(data['login']):
            return {'message': f'{data["login"]} already exists.'}

        user = UserModel(**data)
        user.save_user()
        return {
            'message': f'The user {data["login"]} was successfully created!'
        }, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = atributes.parse_args()
        user = UserModel.find_login(data['login'])
        if user and safe_str_cmp(user.password, data['password']):
            token = create_access_token(user.user_id)
            return {'access_token': token}, 200
        return {'message': 'the username or password is incorrect'}, 401