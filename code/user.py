import sqlite3
from flask_restful import Resource, reqparse

#print("Hello") # every time user.py gets imported, this is run, unless it's commented out

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    # add ability to retrieve data from the database
    @classmethod
    def find_by_username(cls, username): # cls = using the current class instead of hard coding
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?" # where clause filters the results such that username matches the given parameter
        result = cursor.execute(query, (username,)) # parameters always need to be in the form of a tuple, which is why we have a comma after username
        row = result.fetchone()
        if row:
            #user = cls(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):  # cls = using the current class instead of hard coding
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"  # where clause filters the results such that username matches the given parameter
        result = cursor.execute(query, (_id,))  # parameters always need to be in the form of a tuple, which is why we have a comma after username
        row = result.fetchone()
        if row:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type = str,
        required = True,
        help = "This field cannot be blank"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args() # will expect a username and a password

        if User.find_by_username(data['username']): # make sure no duplicates
            return {"message": "A user with that username already exists"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        # data comes from a reqparser
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201