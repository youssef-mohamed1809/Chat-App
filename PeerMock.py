from socket import *
import threading
import time
import select
import logging
from threading import Thread
from PeerChatroom import ChatroomHandler
from MessageFormatter import print_colorized_text,format_messages,play_sound
from PeerOneToOne import PeerClient, PeerServer


                

def sendTCPMessage(tcpClientSocket,message):
    tcpClientSocket.send(message.encode()) 
    return
    
    
def receiveTCPMessage(tcpClientSocket):
    return tcpClientSocket.recv(1024).decode()
    
            
def login(username, password, peerServerPort,tcpClientSocket,registryName,registryPort):
  
    username = username.strip()
    password = password.strip()
   # a login message is composed and sent to registry
    # an integer is returned according to each response
    if validate_username(username) and validate_login_password(password):
        message = "LOGIN " + username + " " + password + " " + str(peerServerPort)
        logging.info("Send to " + registryName + ":" + str(registryPort) + " -> " + message)
        sendTCPMessage(tcpClientSocket, message)        
        response = receiveTCPMessage(tcpClientSocket)
        logging.info("Received from " + registryName + " -> " + response)
        if response == "login-success":
            print("Logged in successfully...")
            return 1
        elif response == "login-account-not-exist":
            print("Account does not exist...")
            return 0
        elif response == "login-online":
            print("Account is already online...")
            return 2
        elif response == "login-wrong-password":
            print_colorized_text("Wrong password...",'RED')
            return 3
            
def validate_username(username):
     try:
         if not username:
             raise ValueError("Username cannot be empty.")
         # Check for short username
         if len(username) < 3:
             raise ValueError("Username is too short. It must be at least 3 characters.")
         # Check for space character in username    
         if ' ' in username:
             raise ValueError("Username cannot contain a space character.")    
         # Check for special characters and numbers in username
        #  if not username.isalpha():
        #      raise ValueError("Username can only contain letters.")
         return True
     except ValueError as e:
         print_colorized_text(f"Error validating username: {e}",'RED')
         logging.error("ValueError: {0}".format(e))
         return False
                                   
def validate_login_password(password):
    try:
        if not password:
             raise ValueError("Password cannot be empty.")
        return True
    except ValueError as e:
         print_colorized_text(f"Error validating username: {e}",'RED')
         logging.error("ValueError: {0}".format(e))
         return False    
    
def validate_password(password):
     try:
         # Check for empty password
         if not password:
             raise ValueError("Password cannot be empty.")
         # Check for short password
         if len(password) < 6:
             raise ValueError("Password is too short. It must be at least 6 characters.")

         # Check for password complexity
         if not any(char.isupper() for char in password):
             raise ValueError("Password must contain at least one uppercase letter.")

#           if not any(char.islower() for char in password):
#               raise ValueError("Password must contain at least one lowercase letter.")

#           if not any(char.isdigit() for char in password):
#               raise ValueError("Password must contain at least one digit.")

#           if not any(char.isascii() and not char.isalnum() for char in password):
#               raise ValueError("Password must contain at least one special character.")
         return True
     except ValueError as e:
         print_colorized_text(f"Error validating password: {e}","RED")
         logging.error("ValueError: {0}".format(e))
         return False
        
#   account creation function
def createAccount(username, password,tcpClientSocket,registryName,registryPort):
    # join message to create an account is composed and sent to registry
    # if response is success then informs the user for account creation
    # if response is exist then informs the user for account existence
    username = username.strip()
    password = password.strip()
   # Validate username
    if validate_username(username) and validate_password(password):
        message = "JOIN " + username + " " + password
        logging.info("Send to " + registryName + ":" + str(registryPort) + " -> " + message)
        sendTCPMessage(tcpClientSocket, message)
        response = receiveTCPMessage(tcpClientSocket)
        logging.info("Received from " + registryName + " -> " + response)
        if response == "join-success":
            print("Account created...")
        elif response == "join-exist":
            print("Account already exists...")
            
# logout function
def logout(option,loginCredentials,timer,tcpClientSocket,registryName,registryPort):
    # a logout message is composed and sent to registry
    # timer is stopped
    if option == 1:
        message = "LOGOUT " + loginCredentials[0]
        timer.cancel()
    else:
        message = "LOGOUT"
    logging.info("Send to " + registryName + ":" + str(registryPort) + " -> " + message)
    sendTCPMessage(tcpClientSocket,message)
    
   
def show_online_users(tcpClientSocket,registryName,registryPort):
    # Send the command to the registry
    message = "SHOW_ONLINE_USERS"
    logging.info("Send to " + registryName + ":" + str(registryPort) + " -> " + message)
    sendTCPMessage( tcpClientSocket,message)
    # Receive and print the response
    response = receiveTCPMessage(tcpClientSocket)
    logging.info("Received from " + registryName + " -> " + response)
    print(response)
        
def create_chatroom(chatroom_name,tcpClientSocket):
        message = f"CREATE_CHATROOM {chatroom_name}"
        sendTCPMessage(tcpClientSocket, message)
        response = receiveTCPMessage(tcpClientSocket)
        response = response.split()
        if response[0] == "room-already-exists":
                    print_colorized_text("Chatroom with similar name already exists...", "RED")
        else:
                    print_colorized_text("Chatroom created successfully...", "GREEN")
        


def searchUser(username,tcpClientSocket):
        # a search message is composed and sent to registry
        # custom value is returned according to each response
        # to this search message
        message = "SEARCH " + username
        tcpClientSocket.send(message.encode())
        response = tcpClientSocket.recv(1024).decode().split()
        if response[0] == "search-success":
            print_colorized_text(username + " is found successfully...","GREEN")
            return response[1]
        elif response[0] == "search-user-not-online":
            print_colorized_text(username + " is not online...","RED")
            return 0
        elif response[0] == "search-user-busy":
            print_colorized_text(username + " is busy...", "RED")
            return 0
        elif response[0] == "search-user-not-found":
            print_colorized_text(username + " is not found","RED")
            return None


def showChatrooms(tcpClientSocket):
    message = "SHOW_CHATROOMS"
    sendTCPMessage(tcpClientSocket,message)
    response =  receiveTCPMessage(tcpClientSocket)
    response = response.split() 
    if response[0] == "show-rooms":
        print("Chat rooms:")
        msg = ''
        for i in range(1, len(response)):
            msg += response[i] +'\n'
        print("\n"+msg + "\n" )
# main process of the peer
class peerMain:

    # peer initializations
    def __init__(self):
        # ip address of the registry
        self.userInput = input("Enter IP address of registry: ").split()
        self.registryName = self.userInput[0]
        # port number of the registry
        self.registryPort = 15600
        # tcp socket connection to registry
        self.tcpClientSocket = socket(AF_INET, SOCK_STREAM)
        
        self.tcpClientSocket.connect((self.registryName,self.registryPort))
        # initializes udp socket which is used to send hello messages
        self.udpClientSocket = socket(AF_INET, SOCK_DGRAM)
        # udp port of the registry
        self.registryUDPPort = 15500
        # login info of the peer
        self.loginCredentials = (None, None)
        # online status of the peer
        self.isOnline = False
        
        self.peerServer = None
        # client of this peer
        self.peerClient = None

        # server port number of this peer
        self.peerServerPort = None
        # timer initialization
        self.timer = None
        
        self.TCPRoomThread = None
        self.UDPRoomThread = None
        self.online_peers = {}
        
    def run(self):
        # log file initialization
        logging.basicConfig(filename="peer.log", level=logging.INFO)
        # as long as the user is not logged out, asks to select an option in the menu
        createAccount(self.userInput[1], self.userInput[2],self.tcpClientSocket,self.registryName,self.registryPort)
        status = login(self.userInput[1], self.userInput[2], self.userInput[3],self.tcpClientSocket,self.registryName,self.registryPort)
                # is user logs in successfully, peer variables are set
        if status == 1:
                    self.isOnline = True
                    self.loginCredentials = (self.userInput[1], self.userInput[2])
                    self.peerServerPort = int(self.userInput[3])
                    # hello message is sent to registry
                    self.peerServer = PeerServer(self.loginCredentials[0], self.peerServerPort)
                    self.peerServer.start()
                    self.sendHelloMessage()
        # if self.timer is not None:
        #         self.timer.cancel()
        logout(2,self.loginCredentials, self.timer,self.tcpClientSocket,self.registryName,self.registryPort)
        self.isOnline = False
        self.loginCredentials = (None, None)
        self.peerServer.isOnline = False
        self.peerServer.tcpServerSocket.close()
        if self.peerClient is not None:
            self.peerClient.tcpClientSocket.close()
        print("Logged out successfully")
        
       
 


    
    # function for sending hello message
    # a timer thread is used to send hello messages to udp socket of registry
    def sendHelloMessage(self):
        message = "HELLO " + self.loginCredentials[0]
        logging.info("Send to " + self.registryName + ":" + str(self.registryUDPPort) + " -> " + message)
        self.udpClientSocket.sendto(message.encode(), (self.registryName, self.registryUDPPort))
        self.timer = threading.Timer(1, self.sendHelloMessage)
        self.timer.start()

if __name__ == "__main__": 
# peer is started
  pm =peerMain()
  pm.run()