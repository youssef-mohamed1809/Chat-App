from pymongo import MongoClient

class DB:
    def __init__(self):
        self.client = MongoClient("192.168.0.5", 27017)
        self.db = self.client.chatapp
        self.accounts = self.db.accounts

    def login(self, username, password):
        if self.does_user_exist(username, password):
           if self.correct_password(username, password):
               return True    
        return False
    def does_user_exist(self, username):
        accounts_cursor = self.accounts.find({"username": username})
        found_accounts = list(accounts_cursor)

        if len(found_accounts) == 0:
            return False
        return True
    
    def register(self, username, password):
        exist = self.does_user_exist(username)
        if not exist:
            self.accounts.insert_one({"username": username, "password": password})

    def correct_password(self, username, password):
        accounts_cursor = self.accounts.find({"username": username})
        found_accounts = list(accounts_cursor)

        if found_accounts[0]['password'] == password:
            return True
        return False

    def view_all_accounts(self):
        for account in self.accounts.find():
            print(account)
            
    

    