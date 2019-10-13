import unittest
import unittest.mock as mock
import re

from node.token import Token

JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1MTYyMzkwMjJ9.tbDepxpstvGdW8TC3G8zg4B6rUYAOvfzdceoH48wgRQ"


class TestToken(unittest.TestCase):

    def setUp(self):
        self.token = Token()

    def test_validate(self):
        self.token.validate(JWT)

    def test_load_token(self):
        read_token = mock.Mock(return_value=JWT)
        self.token.load_token(read_token)

    def test_str(self):
        read_token = mock.Mock(return_value=JWT)
        self.token.load_token(read_token)

        result = str(self.token)
        self.assertEqual(result, JWT)

