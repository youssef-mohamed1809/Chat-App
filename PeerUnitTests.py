import unittest
from unittest.mock import MagicMock,patch
from Peer import login ,logout,createAccount,show_online_users ,create_chatroom,searchUser


class TestLoginFunction(unittest.TestCase):

    def setUp(self):
        
        self.mock_socket = MagicMock()
        self.registryName = "192.168.56.1"
        self.registryPort = 12345

    @patch('Peer.print')
    @patch('Peer.receiveTCPMessage')
    @patch('Peer.validate_username')
    @patch('Peer.validate_password')
    def test_login_success(self, mock_validate_username, mock_validate_password, mock_receive, mock_print):
        mock_validate_username.return_value = True
        mock_validate_password.return_value = True
        mock_receive.return_value = "login-success"
        result = login("ValidUser", "Valid123", 1234, self.mock_socket, self.registryName, self.registryPort)
        self.assertEqual(result, 1)
        mock_print.assert_called_with("Logged in successfully...")

    @patch('Peer.print')
    @patch('Peer.receiveTCPMessage')
    @patch('Peer.validate_username')
    @patch('Peer.validate_password')
    def test_login_account_not_exist(self, mock_validate_username, mock_validate_password, mock_receive, mock_print):
        mock_validate_username.return_value = True
        mock_validate_password.return_value = True
        mock_receive.return_value = "login-account-not-exist"
        result = login("nonexistent_user", "password", 1234, self.mock_socket, self.registryName, self.registryPort)
        self.assertEqual(result, 0)
        mock_print.assert_called_with("Account does not exist...")

    @patch('Peer.print')
    @patch('Peer.receiveTCPMessage')
    @patch('Peer.validate_username')
    @patch('Peer.validate_password')
    def test_login_account_already_online(self, mock_validate_username, mock_validate_password, mock_receive, mock_print):
        mock_validate_username.return_value = True
        mock_validate_password.return_value = True
        mock_receive.return_value = "login-online"
        result = login("online_user", "password123", 1234, self.mock_socket, self.registryName, self.registryPort)
        self.assertEqual(result, 2)
        mock_print.assert_called_with("Account is already online...")

    @patch('Peer.print_colorized_text')
    @patch('Peer.receiveTCPMessage')
    @patch('Peer.validate_username')
    @patch('Peer.validate_password')
    def test_login_wrong_password(self, mock_validate_username, mock_validate_password, mock_receive, mock_print_colorized):
        mock_validate_username.return_value = True
        mock_validate_password.return_value = True
        mock_receive.return_value = "login-wrong-password"
        result = login("valid_user", "wrong_password", 1234, self.mock_socket, self.registryName, self.registryPort)
        self.assertEqual(result, 3)
        mock_print_colorized.assert_called_with("Wrong password...",'RED')


class TestAccountCreation(unittest.TestCase):

    def setUp(self):
        
        self.mock_socket = MagicMock()
        self.registryName = "192.168.56.1"
        self.registryPort = 12345
    
    @patch('Peer.print')
    @patch('Peer.receiveTCPMessage')
    @patch('Peer.validate_username')
    @patch('Peer.validate_password')                           
    def test_create_account_success(self, mock_validate_username, mock_validate_password, mock_receive, mock_print):
        mock_validate_username.return_value = True
        mock_validate_password.return_value = True
        mock_receive.return_value = "join-success"
        createAccount("valid_user", "wrong_password", self.mock_socket, self.registryName, self.registryPort)
        mock_print.assert_called_with("Account created...")

    @patch('Peer.print')
    @patch('Peer.receiveTCPMessage')
    @patch('Peer.validate_username')
    @patch('Peer.validate_password')                           
    def test_create_account_exists(self, mock_validate_username, mock_validate_password, mock_receive, mock_print):
        mock_validate_username.return_value = True
        mock_validate_password.return_value = True
        mock_receive.return_value = "join-exist"
        createAccount("valid_user", "wrong_password", self.mock_socket, self.registryName, self.registryPort)
        mock_print.assert_called_with("Account already exists...")


class TestLogoutFunction(unittest.TestCase):

    def setUp(self):
        
        self.mock_socket = MagicMock()
        self.mock_timer = MagicMock()
        self.registryName = "192.168.56.1"
        self.registryPort = 12345
        self.loginCredentials = ["username", "password"]

    @patch('Peer.sendTCPMessage')
    @patch('Peer.logging')
    def test_logout_with_option_1(self, mock_logging, mock_send):
        logout(1, self.loginCredentials, self.mock_timer, self.mock_socket, self.registryName, self.registryPort)
        
        self.mock_timer.cancel.assert_called_once()
        mock_send.assert_called_with(self.mock_socket, "LOGOUT username")
        mock_logging.info.assert_called_with("Send to 192.168.56.1:12345 -> LOGOUT username")

class TestShowOnlineUsersFunction(unittest.TestCase):

    def setUp(self):
        
        self.mock_socket = MagicMock()
        self.registryName = "registry_host"
        self.registryPort = 12345

    @patch('Peer.print')
    @patch('Peer.receiveTCPMessage')
    @patch('Peer.sendTCPMessage')
    @patch('Peer.logging')
    def test_show_online_users(self, mock_logging, mock_send, mock_receive, mock_print):
        mock_receive.return_value = "Online Users: \nuser1\nuser2\n"
        show_online_users(self.mock_socket, self.registryName, self.registryPort)

        
        mock_send.assert_called_with(self.mock_socket, "SHOW_ONLINE_USERS")
        mock_logging.info.assert_called_with("Received from registry_host -> Online Users: \nuser1\nuser2\n")
        mock_print.assert_called_with('Online Users: \nuser1\nuser2\n')

class TestCreateChatroomFunction(unittest.TestCase):

    def setUp(self):
        self.mock_socket = MagicMock()

    @patch('Peer.print_colorized_text')  
    def test_create_chatroom_already_exists(self, mock_print_colorized_text):
        self.mock_socket.recv.return_value = "room-already-exists".encode()
        create_chatroom("test_chatroom", self.mock_socket)
        self.mock_socket.send.assert_called_with("CREATE_CHATROOM test_chatroom".encode())
        mock_print_colorized_text.assert_called_with("Chatroom with similar name already exists...", "RED")

    @patch('Peer.print_colorized_text')  
    def test_create_chatroom_success(self, mock_print_colorized_text):
     
        self.mock_socket.recv.return_value = "room-create-success".encode()
        create_chatroom("new_chatroom", self.mock_socket)
        self.mock_socket.send.assert_called_with("CREATE_CHATROOM new_chatroom".encode())
        mock_print_colorized_text.assert_called_with("Chatroom created successfully...", "GREEN")

class TestSearchUserFunction(unittest.TestCase):

    def setUp(self):
        self.mock_socket = MagicMock()

    @patch('Peer.print_colorized_text')
    def test_search_user_success(self,mock_print_colorized_text):
        
        self.mock_socket.recv.return_value = "search-success user_ip:user_port".encode()        
        result = searchUser("test_user", self.mock_socket)    
        self.mock_socket.send.assert_called_with("SEARCH test_user".encode())

        self.assertEqual(result, "user_ip:user_port")
        mock_print_colorized_text.assert_any_call("test_user is found successfully...","GREEN")


    @patch('Peer.print_colorized_text')
    def test_search_user_not_online(self,mock_print_colorized_text):
        
        self.mock_socket.recv.return_value = "search-user-not-online".encode()
        result = searchUser("test_user", self.mock_socket)
        self.mock_socket.send.assert_called_with("SEARCH test_user".encode())

        self.assertEqual(result, 0)
        mock_print_colorized_text.assert_called_with("test_user is not online...","RED")



    @patch('Peer.print_colorized_text')
    def test_search_user_not_found(self, mock_print_colorized_text):
        
        self.mock_socket.recv.return_value = "search-user-not-found".encode()
        result = searchUser("test_user", self.mock_socket)

        self.assertIsNone(result)
        mock_print_colorized_text.assert_called_with("test_user is not found","RED")


if __name__ == '__main__':
    unittest.main()

