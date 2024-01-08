from pymongo import MongoClient

# Includes database operations
class DB:
    # db initializations
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['p2p-chat']


    # checks if an account with the username exists
    def is_account_exist(self, username):
        if len(list(self.db.accounts.find({'username': username}))) > 0:
            return True
        else:
            return False
    

    # registers a user
    def register(self, username, password,salt):
        account = {
            "username": username,
            "password": password,
            "salt" : salt
        }
        self.db.accounts.insert_one(account)
    
    
    # retrieves the password for a given username
    def get_password_and_salt(self, username):
        password = self.db.accounts.find_one({"username": username})["password"]
        salt  = self.db.accounts.find_one({"username": username})["salt"]
        return password, salt
    

