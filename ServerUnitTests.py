import unittest
from unittest.mock import patch, MagicMock
from Server import ClientThread, chatrooms 

class TestClientThread(unittest.TestCase):

    @patch('Server.db')
    def setUp(self, mock_db):
        self.client_thread = ClientThread('192.168.52.1', 12345, MagicMock())

    def test_create_room_new_room(self):

        chatrooms.clear()

        response = self.client_thread.createRoom("TestRoom")
        self.assertEqual(response, 'room-create-success')
        self.assertIn("TestRoom", chatrooms)

    def test_create_room_existing_room(self):

        chatrooms.clear()
        chatrooms["TestRoom"] = {}

        response = self.client_thread.createRoom("TestRoom")
        self.assertEqual(response, 'room-already-exists')
        self.assertEqual(len(chatrooms), 1)

if __name__ == '__main__':
    unittest.main()
