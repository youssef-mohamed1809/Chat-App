import socket

PORT = 5000 
HEADER = 64 
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
ADDRESS = (SERVER, PORT)
DISCONNECT = "!DISCONNECT"

def send_message(message):
    encoded_message = message.encode(FORMAT)
    msg_length = len(encoded_message)
    encoded_msg_length = str(msg_length).encode(FORMAT)
    encoded_msg_length += b' ' * (HEADER - len(encoded_msg_length))
    client.send(encoded_msg_length)
    client.send(encoded_message)

def send_login_message(username, password):
    message_type = "Login"
    encoded_message_type = message_type.encode(FORMAT)
    msg_type_length = len(encoded_message_type)
    encoded_msg_type_length = str(msg_type_length).encode(FORMAT)
    encoded_msg_type_length += b' ' * (HEADER - len(encoded_msg_type_length))

    message = f"{username}|{password}"
    encoded_message = message.encode(FORMAT)
    msg_length = len(encoded_message)
    encoded_msg_length = str(msg_length).encode(FORMAT)
    encoded_msg_length += b' ' * (HEADER - len(encoded_msg_length))

    client.send(encoded_msg_type_length)
    client.send(encoded_message_type)
    client.send(encoded_msg_length)
    client.send(encoded_message)


    receive_login_response()

def receive_login_response():
    length = int(client.recv(HEADER).decode(FORMAT))
    if length:
        res = client.recv(length).decode(FORMAT)
        if res == "Success":
            print("Login Success")
        elif res == "Fail":
            print("Login Failed")

def send_register_message(username, password):
    message_type = "Register"
    encoded_message_type = message_type.encode(FORMAT)
    msg_type_length = len(encoded_message_type)
    encoded_msg_type_length = str(msg_type_length).encode(FORMAT)
    encoded_msg_type_length += b' ' * (HEADER - len(encoded_msg_type_length))

    message = f"{username}|{password}"
    encoded_message = message.encode(FORMAT)
    msg_length = len(encoded_message)
    encoded_msg_length = str(msg_length).encode(FORMAT)
    encoded_msg_length += b' ' * (HEADER - len(encoded_msg_length))

    client.send(encoded_msg_type_length)
    client.send(encoded_message_type)
    client.send(encoded_msg_length)
    client.send(encoded_message)


    receive_register_response()

def receive_register_response():
    length = int(client.recv(HEADER).decode(FORMAT))
    if length:
        res = client.recv(length).decode(FORMAT)
        if res == "Success":
            print("Account Created Successfuly")
        elif res == "Fail":
            print("An Error Occurred")


def main():
    print("Welcome, please choose one of the following options: ")
    print("1. Login")
    print("2. Register")
    choice = int(input())
    while choice != 1 and choice != 2:
        choice = int(input("Please choose a valid option: "))
    if choice == 1:
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")

        send_login_message(username, password)
    elif choice == 2:
        username = input("Please enter a unique username: ")
        password = input("Please enter a strong password: ")

        send_register_message(username, password)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect(ADDRESS)
    main()
