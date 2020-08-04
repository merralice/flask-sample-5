# interacting with sqlite
import sqlite3

# you always need a connection and a cursor
connection = sqlite3.connect('data.db') # refers to a file called data.db, which will be our sqlite database

cursor = connection.cursor() # allows you to select and start things in the database. excutes queries and stores results

create_table = "CREATE TABLE users (id int, username text, password text)" # this is a SQL command; () contains column names
cursor.execute(create_table)

user = (1, 'jose', 'asdf')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

users = [
    (2, 'rolf', 'asdf'),
    (3, 'anne', 'xyz')
]

cursor.executemany(insert_query, users)

# retrieve data out
select_query = "SELECT * FROM users" # remember, star gives everything. we can change this to a specific column name
for row in cursor.execute(select_query):
    print(row)

# you always need a commit and a close
# next we need to tell the connection to save changes
connection.commit()
# then close the connection
connection.close()