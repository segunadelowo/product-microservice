import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
import uuid

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', 
        type=str,
        required=True,
        help="Value required."
    )  

    parser.add_argument('category_id', 
        type=int,
        required=True,
        help="Value required."
    )

    parser.add_argument('supplier_id', 
        type=int,
        required=True,
        help="Value required."
    )  

    parser.add_argument('description', 
        type=str,
        required=True,
        help="Value required."
    )

    parser.add_argument('price', 
        type=float,
        required=True,
        help="Value required."
    )    

    parser.add_argument('item_id', 
        type=str,
        required=False,
        help="Value required."
    )  

      

    def get(self, item_id):
        item = ItemModel.find_by_uuid(item_id)
        if item:
            return item.json()
        return {'message':'item not found'}, 404

    def post(self):
        data = Item.parser.parse_args()
        if ItemModel.find_by_name(data['name']):
            return {'message':"A item with name '{}' already exists.".format(data['name'])},400
    
        item = ItemModel(uuid.uuid4().hex, data['category_id'],data['supplier_id'],data['description'],data['price'],data['name'])
    
        try:
            item.save_entity()
        except:
            return {'message':"An error occurred while creating the item."}, 500

        return item.json(), 201

    def delete (self, item_id):
        item = ItemModel.find_by_uuid(item_id)
        if item:
            item.delete_from_db()        
        return {'message':'item deleted'}


    def put(self, item_id):
        data = Item.parser.parse_args()
        
        try:
            item = ItemModel.find_by_uuid(item_id)

            if item:
                item.item_uuid = data['item_id']
                item.category_id = data['category_id']
                item.supplier_id = data['supplier_id']
                item.description = data['description']
                item.price = data['price']
                item.name = data['name']
                item.save_entity()

        except:
                return {"message":"An error occurred updating the item."},500
        return item.json()



class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}