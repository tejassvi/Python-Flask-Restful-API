# import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    JWTManager, 
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_raw_jwt,
    jwt_refresh_token_required)
from resources.blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('ref_id',
                        type=int,
                        required=False,
                        help="This field cannot be left blank!"
                        )
_user_parser.add_argument('fname',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
_user_parser.add_argument('lname',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
_user_parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
_user_parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
_user_parser.add_argument('role',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
_user_parser.add_argument('date',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
# Inherits the class Resource from flask-restful
class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        if (UserModel.find_by_username(data['email'])):
            return {"message": "User with that Email already exists."}, 400
        user = UserModel(data['ref_id'],data['fname'],data['lname'], data['email'],data['password'],data['role'],data['date'])
        user.save_to_db()
        return {"message" : "User created successfully"}, 201


class User(Resource):
    @classmethod
    @jwt_required
    def get(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message" : "User not found"},404
        return user.json()

    @classmethod
    def delete(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message" : "User not found"},404
        user.delete_from_db()
        return {"message" : "User deleted"}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()
        # find user in database
        user = UserModel.find_by_username(data['email'])
        # check password and create access, refresh tokens
        # This is what the Authenticate() function does in jwt
        if user and safe_str_cmp(user.password,data['password']):
            #This is what the Identity() used to do, It used to save user's id by default
            access_token =  create_access_token(identity=user.user_id, fresh=True) 
            refresh_token = create_refresh_token(user.user_id)
            return {
                "access_token"  : access_token,
                "refresh_token" : refresh_token
            },200
        return {"message" : "Invalid Credentials"},401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti'] #jti is "JWT ID", a unique identifier for JWT.
        BLACKLIST.add(jti)
        return {"message" : "Successfully logged out"}, 200



class TokenRefresh(Resource):
    #receives the refresh_token in class UserLogin
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token" : new_token}, 200

