from socket import *
import threading
import select
import logging
import db
from UserAuthentication import UserAuthentication

chatrooms = {}
tcpClientSocket = None
port = None
tcpThreads = None
# This class is used to process the peer messages sent to registry
# for each peer connected to registry, a new client thread is created
class ClientThread(threading.Thread):
   
    
    # initializations for client thread
    def __init__(self, ip, port, tcpClientSocket):
        threading.Thread.__init__(self)
        # ip of the connected peer
        self.ip = ip
        # port number of the connected peer
        self.port = port
        # socket of the peer
        self.tcpClientSocket = tcpClientSocket
        # username, online status and udp server initializations
        self.username = None
        self.peerServerPort = None
        self.isOnline = True
        self.udpServer = None
        self.udpPeerAddress = None
        self.isBusy = False
        print("New thread started for " + ip + ":" + str(port))
        

    def isAccountBusy(self,name):
        if name in tcpThreads:
            return tcpThreads[name].isBusy
        return False
   
    def isAccountOnline(self,name):
        if name in tcpThreads:
            return tcpThreads[name].isOnline
        return False
    def show_online_users(self):
        online_users = [username for username, thread in tcpThreads.items() if thread.isOnline]
        response = "Online Users: \n"
        for user in online_users:
            response += user + '\n'
        logging.info("Send to " + self.ip + ":" + str(self.port) + " -> " + response)
        self.tcpClientSocket.send(response.encode())
    
    def leaveRoom(self, room_name):
        if  room_name in chatrooms and self.username in chatrooms[room_name]:
            del chatrooms[room_name][self.username] 
            for _, (tcp_sock, _) in chatrooms[room_name].items():
                msg = f"USER_LEFT {self.username}"
                tcp_sock.send(msg.encode()) 
            self.isBusy = False
        

    def createRoom(self,room_name):
        if room_name in chatrooms:
            response = 'room-already-exists'
        else:
            chatrooms[room_name] = {}
            response = 'room-create-success'
        return response
    
    def joinChatroom(self,room_name):
        if room_name not in chatrooms:
            response = 'room-not-found'
        else:
            chatrooms[room_name][self.username] = (self.tcpClientSocket, self.udpPeerAddress)
            response = f"joined-room"
            for username, (tcpSocket, udpAddress) in chatrooms[room_name].items():
                if username != self.username:
                    msg = f"USER_JOINED {self.username} {self.udpPeerAddress[0]}:{str(self.udpPeerAddress[1])}"
                    tcpSocket.send(msg.encode())
                    response += f" {username}:{udpAddress[0]}:{udpAddress[1]}"
            self.isBusy = True
        return response
    
    # main of the thread
    def run(self):
        # locks for thread which will be used for thread synchronization
        self.lock = threading.Lock()
        print("Connection from: " + self.ip + ":" + str(port))
        print("IP Connected: " + self.ip)
        logging.info("Connected to peer")
        while True:
            try:
                # waits for incoming messages from peers
                message = self.tcpClientSocket.recv(1024).decode().split()
                if len(message) != 0:    
                    logging.info("Received from " + self.ip + ":" + str(self.port) + " -> " + " ".join(message))            
                    #   JOIN    #
                    if message[0] == "JOIN":
                        # join-exist is sent to peer,
                        # if an account with this username already exists
                        if db.is_account_exist(message[1]):
                            response = "join-exist"
                            print("From-> " + self.ip + ":" + str(self.port) + " " + response)
                            logging.info("Send to " + self.ip + ":" + str(self.port) + " -> " + response)  
                            self.tcpClientSocket.send(response.encode())
                        # join-success is sent to peer,
                        # if an account with this username is not exist, and the account is created
                        else:
                            ua = UserAuthentication()
                            hashed_password,salt = ua.createNewHash(message[2])
                            db.register(message[1],hashed_password,salt )
                            response = "join-success"
                            logging.info("Send to " + self.ip + ":" + str(self.port) + " -> " + response)
                            self.tcpClientSocket.send(response.encode())
                    #   LOGIN    
                    elif message[0] == "LOGIN":
                        # login-account-not-exist is sent to peer,
                        # if an account with the username does not exist
                        if not db.is_account_exist(message[1]):
                            response = "login-account-not-exist"                                              
                            logging.info("Send to " + self.ip + ":" + str(self.port) + " -> " + response)
                            self.tcpClientSocket.send(response.encode())
                        # login-online is sent to peer,
                        # if an account with the username already online
                        elif self.isAccountOnline(message[1]):
                            response = "login-online"
                            logging.info("Send to " + self.ip + ":" + str(self.port) + " -> " + response)
                            self.tcpClientSocket.send(response.encode())
                        # login-success is sent to peer,
                        # if an account with the username exists and not online
                        else:
                            # retrieves the account's password, and checks if the one entered by the user is correct
                            retrievedPass, retrievedSalt = db.get_password_and_salt(message[1])
                            # if password is correct, then peer's thread is added to threads list
                            # peer is added to db with its username, port number, and ip address
                            ua = UserAuthentication()
                            is_valid_password = ua.checkValidity(retrievedPass,retrievedSalt, message[2])
                            if is_valid_password:
                                self.username = message[1]
                                self.lock.acquire()
                                try:
                                    tcpThreads[self.username] = self
                                finally:
                                    self.lock.release()

                                self.peerServerPort = message[3]

                                # login-success is sent to peer,
                                # and a udp server thread is created for this peer, and thread is started
                                # timer thread of the udp server is started
                                response = "login-success"
                                logging.info("Send to " + self.ip + ":" + str(self.port) + " -> " + response)
                                self.tcpClientSocket.send(response.encode())
                                self.udpServer = UDPServer(self.username, self.tcpClientSocket)
                                self.udpServer.start()
                                self.udpServer.timer.start()
                            # if password not matches and then login-wrong-password response is sent                      
                            else:
                                response = "login-wrong-password"
                                logging.info("Send to " + self.ip + ":" + str(self.port) + " -> " + response)
                                self.tcpClientSocket.send(response.encode())
                    #   LOGOUT  #
                    elif message[0] == "LOGOUT":
                        # if user is online,
                        # removes the user from onlinePeers list
                        # and removes the thread for this user from tcpThreads
                        # socket is closed and timer thread of the udp for this
                        # user is cancelled
                        if len(message) > 1 and message[1] is not None and self.isAccountOnline(message[1]):
                            
                            self.lock.acquire()
                            try:
                                if message[1] in tcpThreads:
                                    del tcpThreads[message[1]]
                            finally:
                                self.lock.release()
                            print(self.ip + ":" + str(self.port) + " is logged out")
                            self.tcpClientSocket.close()
                            self.udpServer.timer.cancel()
                            break
                        else:
                            self.tcpClientSocket.close()
                            break
                    elif message[0] == "SEARCH":
                        if db.is_account_exist(message[1]):
                            if self.isAccountOnline(message[1]):
                                if not self.isAccountBusy(message[1]):
                                    peer_info = [tcpThreads[message[1]].ip, tcpThreads[message[1]].peerServerPort]
                                    response = "search-success " + peer_info[0] + ":" + str(peer_info[1])
                                    logging.info("Send to " + self.ip + ":" + str(self.port) + " -> " + response) 
                                    self.tcpClientSocket.send(response.encode())
                                else:
                                    response = "search-user-busy"
                                    logging.info("Send to " + self.ip + ":" + str(self.port) + " -> " + response) 
                                    self.tcpClientSocket.send(response.encode())
                            else:
                                response = "search-user-not-online"
                                logging.info("Send to " + self.ip + ":" + str(self.port) + " -> " + response) 
                                self.tcpClientSocket.send(response.encode())
                        # enters if username does not exist 
                        else:
                            response = "search-user-not-found"
                            logging.info("Send to " + self.ip + ":" + str(self.port) + " -> " + response) 
                            self.tcpClientSocket.send(response.encode())
                    
                    elif message[0] == "SHOW_ONLINE_USERS":
                           self.show_online_users()
                    elif message[0] == 'SHOW_CHATROOMS':
                        message = 'show-rooms ' + ' '.join(chatrooms.keys())
                        self.tcpClientSocket.send(message.encode())
                    elif message[0] == "CREATE_CHATROOM":
                        response = self.createRoom(message[1])
                        self.tcpClientSocket.send(response.encode())
                    elif message[0] == "JOIN_CHATROOM":
                        response = self.joinChatroom(message[1])
                        self.tcpClientSocket.send(response.encode())
                    elif message[0] == "LEAVE_CHATROOM":
                        self.leaveRoom(message[1])
                        msg = f"room-left {message[1]}"
                        tcpClientSocket.send(msg.encode())    
            except OSError as oErr:
                logging.error("OSError: {0}".format(oErr))

    # function for resettin the timeout for the udp timer thread
    def resetTimeout(self):
        self.udpServer.resetTimer()
 
                           
# implementation of the udp server thread for clients
class UDPServer(threading.Thread):
 
 
    # udp server thread initializations
    def __init__(self, username, clientSocket):
        threading.Thread.__init__(self)
        self.username = username
        # timer thread for the udp server is initialized
        self.timer = threading.Timer(3, self.waitHelloMessage)
        self.tcpClientSocket = clientSocket
   
 
    # if hello message is not received before timeout
    # then peer is disconnected
    def waitHelloMessage(self):
        if self.username is not None:
            if self.username in tcpThreads:
                del tcpThreads[self.username]
        self.tcpClientSocket.close()
        print("Removed " + self.username + " from online peers")
 
    # resets the timer for udp server
    def resetTimer(self):
        self.timer.cancel()
        self.timer = threading.Timer(3, self.waitHelloMessage)
        self.timer.start()
 
def runRegistry():
    # tcp and udp server port initializations
    print("Registy started...")
    global port
    port = 15600
    portUDP = 15500
    # db initialization
    global db
    db = db.DB()
    # gets the ip address of this peer
    # first checks to get it for windows devices
    # if the device that runs this application is not windows
    # it checks to get it for macos devices
    hostname=gethostname()
    try:
        host=gethostbyname(hostname)
    except gaierror:
        import netifaces as ni
        host = ni.ifaddresses('en0')[ni.AF_INET][0]['addr']
    print("Registry IP address: " + host)
    print("Registry port number: " + str(port))
    # accounts list for accounts
    accounts = {}
    # tcpThreads list for online client's thread
    global tcpThreads
    tcpThreads = {}
    #tcp and udp socket initializations
    tcpSocket = socket(AF_INET, SOCK_STREAM)
    udpSocket = socket(AF_INET, SOCK_DGRAM)
    tcpSocket.bind((host,port))
    udpSocket.bind((host,portUDP))
    tcpSocket.listen(5)
    # input sockets that are listened
    inputs = [tcpSocket, udpSocket]
    # log file initialization
    logging.basicConfig(filename="registry.log", level=logging.INFO)
    # as long as at least a socket exists to listen registry runs
    while inputs:
        print("Listening for incoming connections...")
        # monitors for the incoming connections
        readable, writable, exceptional = select.select(inputs, [], [])
        for s in readable:
            # if the message received comes to the tcp socket
            # the connection is accepted and a thread is created for it, and that thread is started
            if s is tcpSocket:
                global tcpClientSocket
                tcpClientSocket, addr = tcpSocket.accept()
                newThread = ClientThread(addr[0], addr[1], tcpClientSocket)
                newThread.start()
            # if the message received comes to the udp socket
            elif s is udpSocket:
                # received the incoming udp message and parses it
                message, clientAddress = s.recvfrom(1024)
                message = message.decode().split()
                # checks if it is a hello message
                if message[0] == "HELLO":
                    # checks if the account that this hello message
                    # is sent from is online
                    username = message[1]
                    # if username in server_context.tcpThreads and (ip, int(port)) in server_context.onlinePeers:
                    if username in tcpThreads:
                        tcpThreads[username].resetTimeout()
                        print("Hello is received from " + message[1])
                        logging.info("Received from " + clientAddress[0] + ":" + str(clientAddress[1]) + " -> " + " ".join(message))
                        if tcpThreads[username].udpPeerAddress != clientAddress:
                            tcpThreads[username].udpPeerAddress = clientAddress

    # registry tcp socket is closed
    tcpSocket.close()


if __name__ == "__main__": 
# peer is started
  runRegistry()