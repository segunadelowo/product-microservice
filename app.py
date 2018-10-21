import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
#from resources.item import Item, ItemList
from resources.category import Category, CategoryList
#from resources.supplier import Supplier, SupplierList

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'zxcv'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

#api.add_resource(Supplier, '/suppliers/<string:name>')
#api.add_resource(SupplierList, '/suppliers')
#api.add_resource(Item, '/items/<string:name>')
#api.add_resource(ItemList, '/items')
api.add_resource(Category, '/categories/<string:name>')
api.add_resource(CategoryList, '/categories')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5001)