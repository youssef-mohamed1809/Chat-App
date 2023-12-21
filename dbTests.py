import unittest
from unittest.mock import MagicMock
from db import DB
  
  



class TestDB(unittest.TestCase):

    def setUp(self):
        self.mock_mongo_client = MagicMock()
        self.db = DB()
        self.db.client = self.mock_mongo_client
        self.db.db = self.mock_mongo_client['p2p-chat']


    def test_is_account_exist_true(self):
        self.db.db.accounts.find.return_value = [{"username": "test_user"}]
        result = self.db.is_account_exist("test_user")
        self.assertTrue(result)

    def test_is_account_exist_false(self):
        self.db.db.accounts.find.return_value = []
        result = self.db.is_account_exist("nonexistent_user")
        self.assertFalse(result)

    def test_register(self):
        self.db.register("new_user", "password123", "salt123")
        self.db.db.accounts.insert_one.assert_called_with({"username": "new_user", "password": "password123", "salt": "salt123"})

  
    def test_get_password_and_salt(self):
        self.db.db.accounts.find_one.return_value = {"password": "password123", "salt": "salt123"}
        password, salt = self.db.get_password_and_salt("test_user")
        self.assertEqual(password, "password123")
        self.assertEqual(salt, "salt123")


if __name__ == '__main__':
    unittest.main()
