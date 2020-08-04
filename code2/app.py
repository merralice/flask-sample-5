from flask import Flask #request
from flask_restful import Resource, Api #reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from resources.user import UserRegister # UserRegister is our resource
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # the sqlalchemy db is going to live in the root folder of our project
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'secret'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) # endpoint is /auth; this endpoint returns a JWT token

#items = []

#class Item(Resource):
    #parser = reqparse.RequestParser()
    #parser.add_argument(
    #    'price',
    #    type=float,
    #    required=True,
    #    help="This field cannot be left blank"
    #)

    #@jwt_required() # you can put this in front of any of the functions in this class to require a token
    #def get(self, name):
        #for item in items:
        #    if item['name'] == name:
        #        return item
    #    item = next(filter(lambda x: x['name'] == name, items), None) # filter function does not return an item. next gives first item found by the function
        #return {'item': None}, 404
    #    return {'item': item}, 200 if item is not None else 404

    #def post(self, name): # must have same set of parameters as get
    #    data = Item.parser.parse_args()
    #    if next(filter(lambda x: x['name'] == name, items), None) is not None:
    #        return {'message': "an item with name '{}' already exists".format(name)}, 400 # filter things out first before getting data
        #data = request.get_json() # if you use force=True, you won't need the contenttype header in postman
        # silent=True will return None instead of giving an error

    #    data = Item.parser.parse_args()
        
    #    item = {'name': name, 'price': data['price']} # access the price key of the data dictionary
    #    items.append(item)
    #    return item, 201 # application will know that we made an item; 201 is for created

    #def delete(self, name):
    #    global items
    #    items = list(filter(lambda x: x['name'] != name, items))
    #    return {'message': 'Item deleted'}

    #def put(self, name):
        #data = request.get_json()
    #    data = Item.parser.parse_args() # puts requests with valid arguments in data
    #    print(data['another'])
        # find out if item already exists
    #    item = next(filter(lambda x: x['name'] == name, items), None)
    #    if item is None:
    #        item = {'name': name, 'price': data['price']}
    #        items.append(item)
    #    else:
    #        item.update(data) # item's name changes alongside the update
    #    return item

#class ItemList(Resource):
    #def get(self):
    #    return {'items': items}

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>') # access items like so: http://127.0.0.1:5000/item/Rolf
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__': # circumvents importing issues; only the file that you run is "main"; if this file gets imported, flask app won't run
    from db import db # not sure if I need this; may cause importing issues?
    db.init_app(app)
    app.run(port=5000, debug=True) # port 5000 is the default so this is not actually necessary
