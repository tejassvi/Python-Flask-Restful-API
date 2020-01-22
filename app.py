
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from resources.user import UserRegister,User,UserLogin,TokenRefresh,UserLogout
from resources.item import Item, ItemList
from resources.markers import Marker,MarkerList
from resources.store import Store,StoreList
from resources.blacklist import BLACKLIST

#We do not have to jsonify responses when using Flask-restful because that is already taken care of

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_SECRET_KEY'] = 'tan123'
#Creating a secret key

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

#JWT Manager links to the app but does not create authentication end point
jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin" : True}
    return {"is_admin" : False}

@jwt.token_in_blacklist_loader #Function that returns true, if token is in blacklist
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST
    
@jwt.expired_token_loader #It is called when the token is expired
def expired_token_callback():
    return {
        "description" : "The token has expired",
        "error" : "token_expired"
    }, 401

@jwt.invalid_token_loader #It is called when the token sent in authorization header is not actual JWT
def invalid_token_callback(error):
    return {
        "description" : "Signature verification failed",
        "error" : "invalid_token"
    } , 401

@jwt.unauthorized_loader #It is called when a JWT is not sent at all
def missing_token_callback(error):
    return {
        "description" : "Request does not contain an access token",
        "error" : "authorization_required"
    }, 401

@jwt.needs_fresh_token_loader #It is called when a non-fresh token is sent, but we need a fresh token
def token_not_fresh_callback():
    return {
        "description" : "The token is not fresh",
        "error" : "fresh_token_required"
    }, 401

@jwt.revoked_token_loader # You an revoke a token in JWT, to force log out a user
def revoked_token_callback():
    return {
        "description" : "The token has been revoked",
        "error" : "token_revoked"
    }, 401


api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Marker,'/marker/<int:submittedby_id>') #http://127.0.0.1:5000/marker/<int :submittedby_id>
api.add_resource(MarkerList,'/markers') #http://127.0.0.1:5000/markers
api.add_resource(UserRegister,'/register') #http://127.0.0.1:5000/register
api.add_resource(User,'/user/<int:user_id>')
api.add_resource(TokenRefresh,'/refresh') #Refresh Token Endpoint
api.add_resource(ItemList,'/items')
api.add_resource(UserLogin,'/login')
api.add_resource(Item,'/item/<string:name>')
api.add_resource(UserLogout,'/logout') #http://127.0.0.1:5000/logout

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)