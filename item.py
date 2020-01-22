from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    #Can be used to parse html page fields as well
    parser.add_argument('price',
        type=float,
        required=True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help = "Every item, needs a store ID"
    )

    @jwt_required
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message" : "Item not found"}, 404
    
    @fresh_jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message' : "An item with name {} already exists!".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name,data['price'],data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message" : "An error occurred inserting the item"}, 500 #Internal Server Error
        
        return item.json(), 201

    @jwt_required
    def delete(self,name):
        # claims = get_jwt_claims()
        # if not claims['is_admin']:
        #     return {"message" : "Admin privilege required."}, 401
        item =ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message" : "Item Deleted"}

    #idempotent, put can be used to both create or update an existing item
    def put(self,name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name,data['price'],data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    @jwt_optional 
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.query.all()]
        if user_id:
            return {"items" : items},200
        return {
            "items" : [item['name'] for item in items],
            "message" : "More data available once you login!"
        }, 200