import unittest
from unittest.mock import patch, MagicMock
from Peer import peerMain

class TestPeerLoginIntegration(unittest.TestCase):

    @patch('Peer.input', side_effect=['192.168.56.1','2', 'my_username', 'my_password', '12345', '3'])
    @patch('Peer.print_colorized_text')
    @patch('Peer.socket')
    @patch('Peer.validate_username', return_value=True)
    @patch('Peer.validate_login_password', return_value=True)
    @patch('Peer.sendTCPMessage')
    @patch('Peer.receiveTCPMessage')
    @patch('Peer.PeerServer')
    def test_peer_login(self, mock_PeerServer,mock_receiveTCPMessage, mock_sendTCPMessage, mock_validate_password, mock_validate_username, mock_socket_class, mock_print_colorized_text, mock_input):
        

        mock_receiveTCPMessage.side_effect = ["login-success", "logout-success"]

        peer_instance = peerMain()
        peer_instance.run()
  

        expected_login_message = "LOGIN my_username my_password 12345"
        mock_sendTCPMessage.assert_any_call(peer_instance.tcpClientSocket, expected_login_message)

        expected_logout_message = "LOGOUT my_username"
        mock_sendTCPMessage.assert_any_call(peer_instance.tcpClientSocket, expected_logout_message)

        self.assertTrue(not peer_instance.isOnline) 
 

class TestPeerLoginAndCreateChatroomIntegration(unittest.TestCase):

    @patch('Peer.input', side_effect=['192.168.56.1', '2', 'my_username', 'my_password', '12345', '7', 'chatroom_name', '3'])
    @patch('Peer.print_colorized_text')
    @patch('Peer.socket')
    @patch('Peer.validate_username', return_value=True)
    @patch('Peer.validate_login_password', return_value=True)
    @patch('Peer.sendTCPMessage')
    @patch('Peer.receiveTCPMessage')
    @patch('Peer.PeerServer')
    def test_peer_login_and_create_chatroom(self, mock_PeerServer, mock_receiveTCPMessage, mock_sendTCPMessage, mock_validate_password, mock_validate_username, mock_socket_class, mock_print_colorized_text, mock_input):
        
        mock_receiveTCPMessage.side_effect = ["login-success", "create-chatroom-success", "logout-success"]

        peer_instance = peerMain()
        peer_instance.run()
  
        expected_login_message = "LOGIN my_username my_password 12345"
        mock_sendTCPMessage.assert_any_call(peer_instance.tcpClientSocket, expected_login_message)

        expected_create_chatroom_message = "CREATE_CHATROOM chatroom_name"
        mock_sendTCPMessage.assert_any_call(peer_instance.tcpClientSocket, expected_create_chatroom_message)

        expected_logout_message = "LOGOUT my_username"
        mock_sendTCPMessage.assert_any_call(peer_instance.tcpClientSocket, expected_logout_message)


if __name__ == '__main__':
    unittest.main()
