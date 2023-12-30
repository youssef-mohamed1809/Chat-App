import unittest
from unittest.mock import MagicMock,patch
from peer import login ,logout,createAccount,show_online_users 






class TestLoginFunction(unittest.TestCase):

    def setUp(self):
        # Mock the tcpClientSocket
        self.mock_socket = MagicMock()
        self.registryName = "192.168.56.1"
        self.registryPort = 12345

    @patch('peer.print')
    @patch('peer.receiveTCPMessage')
    @patch('peer.validate_username')
    @patch('peer.validate_password')
    def test_login_success(self, mock_validate_username, mock_validate_password, mock_receive, mock_print):
        mock_validate_username.return_value = True
        mock_validate_password.return_value = True
        mock_receive.return_value = "login-success"
        result = login("ValidUser", "Valid123", 1234, self.mock_socket, self.registryName, self.registryPort)
        self.assertEqual(result, 1)
        mock_print.assert_called_with("Logged in successfully...")

    @patch('peer.print')
    @patch('peer.receiveTCPMessage')
    @patch('peer.validate_username')
    @patch('peer.validate_password')
    def test_login_account_not_exist(self, mock_validate_username, mock_validate_password, mock_receive, mock_print):
        mock_validate_username.return_value = True
        mock_validate_password.return_value = True
        mock_receive.return_value = "login-account-not-exist"
        result = login("nonexistent_user", "password", 1234, self.mock_socket, self.registryName, self.registryPort)
        self.assertEqual(result, 0)
        mock_print.assert_called_with("Account does not exist...")

    @patch('peer.print')
    @patch('peer.receiveTCPMessage')
    @patch('peer.validate_username')
    @patch('peer.validate_password')
    def test_login_account_already_online(self, mock_validate_username, mock_validate_password, mock_receive, mock_print):
        mock_validate_username.return_value = True
        mock_validate_password.return_value = True
        mock_receive.return_value = "login-online"
        result = login("online_user", "password123", 1234, self.mock_socket, self.registryName, self.registryPort)
        self.assertEqual(result, 2)
        mock_print.assert_called_with("Account is already online...")

    @patch('peer.print_colorized_text')
    @patch('peer.receiveTCPMessage')
    @patch('peer.validate_username')
    @patch('peer.validate_password')
    def test_login_wrong_password(self, mock_validate_username, mock_validate_password, mock_receive, mock_print_colorized):
        mock_validate_username.return_value = True
        mock_validate_password.return_value = True
        mock_receive.return_value = "login-wrong-password"
        result = login("valid_user", "wrong_password", 1234, self.mock_socket, self.registryName, self.registryPort)
        self.assertEqual(result, 3)
        mock_print_colorized.assert_called_with("Wrong password...",'RED')


class TestAccountCreation(unittest.TestCase):

    def setUp(self):
        # Mock the socket
        self.mock_socket = MagicMock()
        self.registryName = "192.168.56.1"
        self.registryPort = 12345
    
    @patch('peer.print')
    @patch('peer.receiveTCPMessage')
    @patch('peer.validate_username')
    @patch('peer.validate_password')                           
    def test_create_account_success(self, mock_validate_username, mock_validate_password, mock_receive, mock_print):
        mock_validate_username.return_value = True
        mock_validate_password.return_value = True
        mock_receive.return_value = "join-success"
        createAccount("valid_user", "wrong_password", self.mock_socket, self.registryName, self.registryPort)
        mock_print.assert_called_with("Account created...")

    @patch('peer.print')
    @patch('peer.receiveTCPMessage')
    @patch('peer.validate_username')
    @patch('peer.validate_password')                           
    def test_create_account_exists(self, mock_validate_username, mock_validate_password, mock_receive, mock_print):
        mock_validate_username.return_value = True
        mock_validate_password.return_value = True
        mock_receive.return_value = "join-exist"
        createAccount("valid_user", "wrong_password", self.mock_socket, self.registryName, self.registryPort)
        mock_print.assert_called_with("Account already exists...")


class TestLogoutFunction(unittest.TestCase):

    def setUp(self):
        # Mock the tcpClientSocket and timer
        self.mock_socket = MagicMock()
        self.mock_timer = MagicMock()
        self.registryName = "192.168.56.1"
        self.registryPort = 12345
        self.loginCredentials = ["username", "password"]

    @patch('peer.sendTCPMessage')
    @patch('peer.logging')
    def test_logout_with_option_1(self, mock_logging, mock_send):
        logout(1, self.loginCredentials, self.mock_timer, self.mock_socket, self.registryName, self.registryPort)
        
        # Check if the timer's cancel method was called
        self.mock_timer.cancel.assert_called_once()

        # Check if the correct logout message was sent
        mock_send.assert_called_with(self.mock_socket, "LOGOUT username")

        # Check if the logging was called with the correct message
        mock_logging.info.assert_called_with("Send to 192.168.56.1:12345 -> LOGOUT username")

class TestShowOnlineUsersFunction(unittest.TestCase):

    def setUp(self):
        # Mock the tcpClientSocket
        self.mock_socket = MagicMock()
        self.registryName = "registry_host"
        self.registryPort = 12345

    @patch('peer.print')
    @patch('peer.receiveTCPMessage')
    @patch('peer.sendTCPMessage')
    @patch('peer.logging')
    def test_show_online_users(self, mock_logging, mock_send, mock_receive, mock_print):
        mock_receive.return_value = "Online Users: \nuser1\nuser2\n"
        show_online_users(self.mock_socket, self.registryName, self.registryPort)

        # Check if the correct message was sent
        mock_send.assert_called_with(self.mock_socket, "SHOW_ONLINE_USERS")

        mock_logging.info.assert_called_with("Received from registry_host -> Online Users: \nuser1\nuser2\n")

        # Check if the print function was called with the correct response
        mock_print.assert_called_with('Online Users: \nuser1\nuser2\n')


if __name__ == '__main__':
    unittest.main()

