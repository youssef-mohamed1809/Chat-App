import logging
import select
from MessageFormatter import print_colorized_text
      


class ChatroomHandler:
    def __init__(self):
      self.running = True

    def tcpChatHandler(self, peer):
        inputs = [peer.tcpClientSocket]
        while inputs and self.running:
            try:
                readable, _, _ = select.select(inputs, [], [],0.2)
                if not readable:
                    continue
                message = peer.tcpClientSocket.recv(1024).decode().split() 
                if not message:
                    continue
                if message[0] == "JOINED":
                    peer.online_peers[message[1]] = (message[2].split(":")[0], int(message[2].split(":")[1]))
                    print_colorized_text(message[1], "YELLOW",'')
                    print(" joined the chat...")
                elif message[0] == "LEFT":
                    if message[1] in peer.online_peers:
                        del peer.online_peers[message[1]]
                    print_colorized_text(message[1], "YELLOW",'')
                    print(" left the chat..")

            except OSError as oErr:
                logging.error("OSError: {0}".format(oErr))



    def udpChatHandler(self,peer):
        inputs = [peer.udpClientSocket]
        while inputs and self.running:
            readable, _, _ = select.select(inputs, [], [],0.2)
            for s in readable:
                if s is peer.udpClientSocket:
                    message, clientAddress = peer.udpClientSocket.recvfrom(1024)
                    temp = message.decode().split()
                    username = temp[0]
                    message_content = " ".join(temp[1:])
                    if username not in peer.online_peers:
                        peer.online_peers[username] = clientAddress
                    print_colorized_text(username+":", "YELLOW", '')
                    print(message_content)

    def broadcast_message(self,peer, message):
        for _, address in peer.online_peers.items():
            peer.udpClientSocket.sendto(str(peer.loginCredentials[0] + " " + message).encode(), address)

