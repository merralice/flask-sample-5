import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True) # primary key means that this is auto-incrementing
    username = db.Column(db.String(80)) # limit size of username
    password = db.Column(db.String(80))

    def __init__(self, _id, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # add ability to retrieve data from the database
    @classmethod
    def find_by_username(cls, username): # cls = using the current class instead of hard coding
        return cls.query.filter_by(username=username).first() # get the first row returned
        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()

        #query = "SELECT * FROM users WHERE username=?" # where clause filters the results such that username matches the given parameter
        #result = cursor.execute(query, (username,)) # parameters always need to be in the form of a tuple, which is why we have a comma after username
        #row = result.fetchone()
        #if row:
        #    #user = cls(row[0], row[1], row[2])
        #    user = cls(*row)
        #else:
        #    user = None

        #connection.close()
        #return user

    @classmethod
    def find_by_id(cls, _id):  # cls = using the current class instead of hard coding
        return cls.query.filter_by(id=_id).first()
        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()

        #query = "SELECT * FROM users WHERE id=?"  # where clause filters the results such that username matches the given parameter
        #result = cursor.execute(query, (_id,))  # parameters always need to be in the form of a tuple, which is why we have a comma after username
        #row = result.fetchone()
        #if row:
        #    # user = cls(row[0], row[1], row[2])
        #    user = cls(*row)
        #else:
        #    user = None

        #connection.close()
        #return user