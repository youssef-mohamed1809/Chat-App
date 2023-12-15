import socket
import threading
import db


#CONSTANTS#
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5000
FORMAT = 'utf-8'
ADDRESS = (SERVER, PORT)
DISCONNECT = "!DISCONNECT"


db = db.DB()
# Whenever a client connects
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        # Get from the client the message length they want to send
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            # Get the actual message
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == "Login":
                msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(FORMAT)
                    print(msg)
            if msg == DISCONNECT:
                connected = False
            print(f"[{addr}] {msg}")
    conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    print("STARTING SERVER")
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
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")        


