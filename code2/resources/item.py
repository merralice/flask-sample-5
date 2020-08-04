from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="Every item needs a store id"
    )

    @jwt_required()  # you can put this in front of any of the functions in this class to require a token
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404


        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()

        #query = "SELECT * FROM items WHERE name=?"
        #result = cursor.execute(query, (name,))
        #row = result.fetchone() # will give us the only row with a specific name
        #connection.close()

        #if row:
        #    return {'item': {'name': row[0], 'price': row[1]}}
        #else: # technically this else statement is optional
        #    return {'message': 'Item not found'}, 404

    def post(self, name):  # must have same set of parameters as get
        #data = Item.parser.parse_args()
        #if next(filter(lambda x: x['name'] == name, items), None): #is not None:
        #    return {'message': "an item with name '{}' already exists".format(name)}, 400  # filter things out first before getting data
        # data = request.get_json() # if you use force=True, you won't need the contenttype header in postman
        # silent=True will return None instead of giving an error

        if ItemModel.find_by_name(name):
            return {'message': "An item with the name {} already exists".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)  # access the price key of the data dictionary

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting this item."}, 500 # internal server error
        #items.append(item)
        return item.json(), 201  # application will know that we made an item; 201 is for created

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}
        return {'message': 'Item not found'}, 404

        #global items
        #items = list(filter(lambda x: x['name'] != name, items))

        # without SQLAlchemy:
        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()

        #query = "DELETE FROM items WHERE name=?" # if you don't have the WHERE clause, you will delete everything from the table
        #cursor.execute(query, (name,))

        #connection.commit()
        #connection.close()
        # items.append(item)



    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()  # puts requests with valid arguments in data
        # find out if item already exists
        #item = next(filter(lambda x: x['name'] == name, items), None)
        item = ItemModel.find_by_name(name) # find item in database
        #updated_item = ItemModel(name, data['price'])

        if item is None:
            item = ItemModel(name, **data)
            #item = {'name': name, 'price': data['price']}
            #try:
            #    updated_item.save_to_db()
            #except:
            #    return {"message": "An error occurred inserting this item"}, 500
        else:
            #try:
            #    updated_item.save_to_db()
            #except:
            #    return {"message": "An error occurred updating the item"}, 500
            item.price = data['price']
            #item.store_id = data['store_id']

        item.save_to_db()
        return item.json() # instead of updated_item.json()

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]} # using list comprehension
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))} # using lambda function; good to use if you have to combine with another language
        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()

        #query = "SELECT * FROM items"
        #result = cursor.execute(query) # we can iterate over the result
        #items = []
        #for row in result:
        #    items.append({'name': row[0], 'price': row[1]})

        #connection.close()
        #return {'items': items}