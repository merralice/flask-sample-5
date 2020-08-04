import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )

    @jwt_required()  # you can put this in front of any of the functions in this class to require a token
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
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

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):  # must have same set of parameters as get
        #data = Item.parser.parse_args()
        #if next(filter(lambda x: x['name'] == name, items), None): #is not None:
        #    return {'message': "an item with name '{}' already exists".format(name)}, 400  # filter things out first before getting data
        # data = request.get_json() # if you use force=True, you won't need the contenttype header in postman
        # silent=True will return None instead of giving an error

        if self.find_by_name(name):
            return {'message': "An item with the name {} already exists".format(name)}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}  # access the price key of the data dictionary

        try:
            self.insert(item)
        except:
            return {"message": "An error occurred inserting this item."}, 500 # internal server error
        #items.append(item)
        return item, 201  # application will know that we made an item; 201 is for created

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self, name):
        #global items
        #items = list(filter(lambda x: x['name'] != name, items))

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?" # if you don't have the WHERE clause, you will delete everything from the table
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        # items.append(item)

        return {'message': 'Item deleted'}

    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()  # puts requests with valid arguments in data
        # find out if item already exists
        #item = next(filter(lambda x: x['name'] == name, items), None)
        item = self.find_by_name(name) # find item in database
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            #item = {'name': name, 'price': data['price']}
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occurred inserting this item"}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occurred updating the item"}, 500
        return item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query) # we can iterate over the result
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()
        return {'items': items}