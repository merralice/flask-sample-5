from models.user import UserModel
# from werkzeug.security import safe_str_cmp

#users = [
#    {
#        'id': 1,
#        'username': 'bob',
#        'password': 'asdf'
#    }
#]

# improved:
users = [
    UserModel(1, 'merr', 'asdf')
]

#username_mapping = { 'bob': {
#        'id': 1,
#        'username': 'bob',
#        'password': 'asdf'
#    }
#}

# improved:
username_mapping = {u.username: u for u in users} # comprehension; assigning key value pairs

#userid_mapping = { 1: {
#        'id': 1,
#        'username': 'bob',
#        'password': 'asdf'
#    }
#}

# improved:
userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    user = UserModel.find_by_username(username)
    #user = username_mapping.get(username, None) # None is the default value
    # can also use:
    # if user and safe_str_cmp(user.password, password):
    if user and user.password == password: # if you're using python 2.7, don't compare strings with ==
        return user

def identity(payload): # unique to flask-jwt; uses JWT token to get the correct user id that the token represents
    user_id = payload['identity']
    #return userid_mapping.get(user_id, None)
    return UserModel.find_by_id(user_id)