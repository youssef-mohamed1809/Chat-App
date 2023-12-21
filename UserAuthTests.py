import unittest
from unittest.mock import patch
from UserAuthentication import UserAuthentication



class TestUserAuthentication(unittest.TestCase):

    def setUp(self):
        self.user_auth = UserAuthentication()

    @patch('UserAuthentication.bcrypt.hashpw')
    def test_hashPassword(self, mock_hashpw):
        mock_hashpw.return_value = b"hashed_password"
        salt = b"salt"
        result = self.user_auth.hashPassword("message", salt)
        self.assertEqual(result, b"hashed_password")
        mock_hashpw.assert_called_with(b"pepper_hashmessage" + salt.decode("utf-8").encode('utf-8'), salt)

    @patch('UserAuthentication.bcrypt.gensalt')
    @patch('UserAuthentication.bcrypt.hashpw')
    def test_createNewHash(self, mock_hashpw, mock_gensalt):
        mock_gensalt.return_value = b"salt"
        mock_hashpw.return_value = b"hashed_password"
        hashed_password, salt = self.user_auth.createNewHash("message")
        self.assertEqual(hashed_password, b"hashed_password")
        self.assertEqual(salt, b"salt")
        mock_gensalt.assert_called_once()
        mock_hashpw.assert_called_with(b"pepper_hashmessage" + b"salt".decode("utf-8").encode('utf-8'), b"salt")

    @patch('UserAuthentication.bcrypt.hashpw')
    def test_checkValidity(self, mock_hashpw):
        mock_hashpw.return_value = b"hashed_password"
        salt = b"salt"
        self.assertTrue(self.user_auth.checkValidity(b"hashed_password", salt, "message"))
        self.assertFalse(self.user_auth.checkValidity(b"wrong_hashed_password", salt, "message"))



if __name__ == '__main__':
    unittest.main()
