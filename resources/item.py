from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float, 
        required=True, 
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id."
    )

    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "item name not found"}, 404 #Not Found

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "Item named '{}' already exists.".format(name)}, 400 #Bad Request

        data = Item.parser.parse_args()
        
        item = ItemModel(name, **data) #data['price'], data['store_id']

        try:
            item.upsert_to_db()
        except:
            return {"message": "An error ocurred inserting the item."}, 500 #Internal Server Error

        return item.json(), 201 #Created

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item has been deleted'}
        else:
            return {"message": "Item '{}' doesn't exists".format(name)}, 400 #Bad Request

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            try:
                item = ItemModel(name, **data) # data['price'], data['store_id']
            except:
                return {"message": "An error have ocurred inserting the item."}, 500 #Internal Server Error
        else:
            try:
                item.price = data['price']
                item.store_id = data['store_id']
            except:
                return {"message": "An error have ocurred updating the item."}, 500 #Internal Server Error
        
        item.upsert_to_db()
        
        return item.json()
