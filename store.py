from flask_restful import Resource
from models.store import StoreModel
from flask_jwt_extended import jwt_required,get_jwt_claims

class Store(Resource):
    # parser = reqparse.RequestParser()
    # #Can be used to parse html page fields as well
    # parser.add_argument('name',
    #     type=String,
    #     required=True,
    #     help = "This field cannot be left blank!"
    # )

    @jwt_required
    def get(self,name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {"message" : "Admin privilege required."}, 401
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message" : "Store not found"}, 404
    
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message" : "This store with name '{}' already exists".format(name)},400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message" : "An error occurred while creating the store"},500

        return store.json(),201

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message" : "Store Deleted"}
        else:
            return {"message" : "The store that you are trying to delete does not even exist LOL"}


class StoreList(Resource):
    def get(self):
        return {'stores':[store.json for store in StoreModel.query.all()]}
        