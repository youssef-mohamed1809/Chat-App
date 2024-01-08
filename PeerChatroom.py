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
                msg = peer.tcpClientSocket.recv(1024).decode().split() 
                if not msg:
                    continue
                if msg[0] == "USER_JOINED":
                    peer.online_peers[msg[1]] = (msg[2].split(":")[0], int(msg[2].split(":")[1]))
                    print_colorized_text(msg[1], "YELLOW",'')
                    print(" joined the chat...")
                elif msg[0] == "USER_LEFT":
                    if msg[1] in peer.online_peers:
                        del peer.online_peers[msg[1]]
                    print_colorized_text(msg[1], "YELLOW",'')
                    print(" left the chat..")

            except OSError as oErr:
                logging.error("OSError: {0}".format(oErr))



    def udpChatHandler(self,peer):
        inputs = [peer.udpClientSocket]
        while inputs and self.running:
            readable, _, _ = select.select(inputs, [], [],0.2)
            for s in readable:
                if s is peer.udpClientSocket:
                    msg, clientAddress = peer.udpClientSocket.recvfrom(1024)
                    msg_split = msg.decode().split()
                    username = msg_split[0]
                    msg_content = " ".join(msg_split[1:])
                    if username not in peer.online_peers:
                        peer.online_peers[username] = clientAddress
                    print_colorized_text(username+":", "YELLOW", '')
                    print(msg_content)

    def broadcastMessage(self,peer, message):
        for _, address in peer.online_peers.items():
            peer.udpClientSocket.sendto(str(peer.loginCredentials[0] + " " + message).encode(), address)

