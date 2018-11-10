from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask import jsonify

from security import authenticate, identity as identity_function

#note: import your models to enable SQLALCHEMY be aware of them for tbl creation
#from resources.item import Item, ItemList
from resources.user import UserRegister
from resources.category import Category, CategoryList
from resources.item import Item, ItemList

#import sentry_sdk
#from sentry_sdk.integrations.flask import FlaskIntegration

#sentry_sdk.init(
#    dsn="https://aedb9936570242d682cdd1321baf4eae@sentry.io/1305565",
#    integrations=[FlaskIntegration()]
#) 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #can also connect to postgress, oracle, mysql
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key = '1111' 
api = Api(app)

@app.before_first_request
def create_tables(): # creates the tables when app starts, instead of maully running scripts
    db.create_all()

# configuration 
# More options https://pythonhosted.org/Flask-JWT/
# app.config['JWT_AUTH_URL_RULE'] = '/login' if you dont want /auth

# config JWT to expire within half an hour
#app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

# config JWT auth key name to be 'email' instead of default 'username'
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

# security setup for the /auth endpoint
jwt = JWT(app, authenticate, identity_function)

# customize JWT auth response, include user_id in response body.
# it is generally not recommended to include information that is encrypted in the access_token 
# since it may introduce security issues.
@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
                        'access_token': access_token.decode('utf-8'),
                        'user_id': identity.id
                   })

# customize JWT auth response
# By default, Flask-JWT raises JWTError when an error occurs within any of the handlers (e.g. during authentication, 
# identity, or creating the response). In some cases we may want to customize what our Flask app does when such an error occurs. We can do it this way
#@jwt.error_handler
#def customized_error_handler(error):
#    return jsonify({
#                       'message': error.description,
#                       'code': error.status_code
#                   }), error.status_code

# routes
api.add_resource(Category, '/api/v1/categories/<string:category_id>') # GET,PUT,DELETE
api.add_resource(CategoryList, '/api/v1/categories') #GET,POST

api.add_resource(ItemList, '/api/v1/items')
api.add_resource(Item, '/api/v1/items/<string:item_id>')

api.add_resource(UserRegister,'/api/v1/register')

if __name__ == '__main__': # only run on startup, if this file is called by another file dont run code below
    from db import db # this is to prevent circle imports hence import here
    db.init_app(app) 
    app.run(port=5001, debug=True)