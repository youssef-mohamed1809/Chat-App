import socket
import threading
import db

#CONSTANTS#
DB = db.DB()
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5000
FORMAT = 'utf-8'
ADDRESS = (SERVER, PORT)
DISCONNECT = "!DISCONNECT"

def handle_login():
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        
        username = ""
        password = ""
        count = 0

        while msg[count] != '|':
            username += msg[count]
            count += 1
        password = msg[count+1:]

        login, msg = DB.login(username, password)

        response = ""
        if login:
            response = "Success"
        else:
            response = msg

        encoded_response = response.encode(FORMAT)
        msg_length = len(encoded_response)
        encoded_msg_length = str(msg_length).encode(FORMAT)
        encoded_msg_length += b' ' * (HEADER - len(encoded_msg_length))

        conn.send(encoded_msg_length)
        conn.send(encoded_response)

def handle_register():
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        
        username = ""
        password = ""
        count = 0

        while msg[count] != '|':
            username += msg[count]
            count += 1
        password = msg[count+1:]

        register = DB.register(username, password)

        response = ""
        if register:
            response = "Success"
        else:
            response = "User already exists"

        encoded_response = response.encode(FORMAT)
        msg_length = len(encoded_response)
        encoded_msg_length = str(msg_length).encode(FORMAT)
        encoded_msg_length += b' ' * (HEADER - len(encoded_msg_length))

        conn.send(encoded_msg_length)
        conn.send(encoded_response)

# Whenever a client connects
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        # Get from the client the message length they want to send
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == "Login":
                handle_login()
            elif msg == "Register":
                handle_register()
            elif msg == DISCONNECT:
                connected = False
    conn.close()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    print("STARTING SERVER")
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the IP address and Port number to this server and start listening
    server.bind(ADDRESS)
    server.listen()
    print(f"Server is listening on {SERVER} and port {PORT}")
    while True:
        #Accept the incoming connection
        conn, addr = server.accept()
        # Run the handle_client function in a new thread to allow multiple users connected at the same time
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()        


