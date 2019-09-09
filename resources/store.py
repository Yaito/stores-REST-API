from flask_restful import Resource, reqparse

from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store name not found.'}, 404 #Not Found
    
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "Store '{}' already exists.".format(name)}, 400 #Bad Request

        store = StoreModel(name)
        try:
            store.upsert_to_db()
        except:
            return {'message': "An error occurred when creating the store."}, 500 #Internal Server Error
        
        return store.json(), 201 #Created

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db()
                return {"message": "Store deleted"}
            except:
                return {'message': "An error occurred when deleting the store '{}'.".format(name)}, 500 #Internal Server Error
        
        return {'message': "Store '{}' not found.".format(name)}, 404 #Not Found
    
            
    
class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.find_all()]}