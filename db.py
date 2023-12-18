from pymongo import MongoClient
import bcrypt

class DB:
    PEPPER = "pepperoni"
    
    def __init__(self):
        self.client = MongoClient("192.168.0.5", 27017)
        self.db = self.client.chatapp
        self.accounts = self.db.accounts

    def login(self, username, password):
        if self.does_user_exist(username):
           if self.correct_password(username, password):
               return True,""
           else:
               return False, "Incorrect Password"
        return False, "Username doesn't exist"
    
    def does_user_exist(self, username):
        accounts_cursor = self.accounts.find({"username": username})
        found_accounts = list(accounts_cursor)

        return len(found_accounts) > 0
    
    
    def register(self, username, password):
        exist = self.does_user_exist(username)
        if not exist:
            salt = bcrypt.gensalt()
            
            hashed_password = bcrypt.hashpw((self.PEPPER+password+salt).encode('utf-8'), salt)
            self.accounts.insert_one({"username": username, "password": hashed_password,"salt": salt})
            return True
        return False
    def correct_password(self, username, password):
        accounts_cursor = self.accounts.find({"username": username})
        found_accounts = list(accounts_cursor)

        if len(found_accounts) > 0:
            stored_salt = found_accounts[0]['salt']
            hashed_password_from_db = bcrypt.hashpw((self.PEPPER + password + stored_salt).encode('utf-8'), stored_salt)
            
            return hashed_password_from_db == found_accounts[0]['password']
        
        return False

    def view_all_accounts(self):
        for account in self.accounts.find():
            print(account)
            
    

    