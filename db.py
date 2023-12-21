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
    
    # checks if an account with the username online
    def is_account_online(self, username):
        if len(list(self.db.online_peers.find({"username": username}))) > 0:
            return True
        else:
            return False
    
    
    # logs in the user
    def user_login(self, username, ip, port):
        online_peer = {
            "username": username,
            "ip": ip,
            "port": port
        }
        self.db.online_peers.insert_one(online_peer)
    

    # logs out the user 
    def user_logout(self, username):
        self.db.online_peers.delete_one({"username": username})
    

    # retrieves the ip address and the port number of the username
    def get_peer_ip_port(self, username):
        res = self.db.online_peers.find_one({"username": username})
        return (res["ip"], res["port"])