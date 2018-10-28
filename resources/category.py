import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.category import CategoryModel
import uuid

class Category(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', 
        type=str,
        required=True,
        help="Value required."
    )  

    def get(self, category_id):
        category = CategoryModel.find_by_uuid(category_id)
        if category:
            return category.json()
        return {'message':'category not found'}, 404

    def post(self):
        data = Category.parser.parse_args()
        if CategoryModel.find_by_name(data['name']):
            return {'message':"A category with name '{}' already exists.".format(data['name'])},400

        category = CategoryModel(uuid.uuid4().hex, data['name'])
        try:
            category.save_entity()
        except:
            return {'message':"An error occurred while creating the category."}, 500

        return category.json(), 201

    def delete (self, category_id):
        category = CategoryModel.find_by_uuid(category_id)
        if category:
            category.delete_from_db()        
        return {'message':'category deleted'}


    def put(self, category_id):
        data = Category.parser.parse_args()
        category = CategoryModel.find_by_uuid(category_id)

        if category:
            category.name = data['name']
            category.save_entity()

           #try:
           #    category.name = data['name']
           #    category.save_to_db()
           #except:
               #return {"message":"An error occurred updating the category."},500
        return category.json()





class CategoryList(Resource):
    def get(self):
        return {'categories': [category.json() for category in CategoryModel.query.all()]}