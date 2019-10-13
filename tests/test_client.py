import unittest
import unittest.mock as mock

from node.client import Client


class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = Client("xxxx", "127.0.0.1:80", "http")
        self.requests = mock.Mock()

    def test_get_job(self):
        response = mock.Mock()
        response.status_code = 200
        payload = {
            "instantiated_job_id": "yyyy",
            "action": "ping",
            "parameters":
            {
                "ip": "127.0.0.1"
            }
        }

        response.json = mock.Mock(return_value=payload)
        self.requests.get = mock.Mock(return_value=response)

        result = self.client.get_job(_requests=self.requests)

        expected = ("yyyy", "ping", {"ip":"127.0.0.1"})

        self.assertEqual(result, expected)

    def test_get_job_no_job(self):
        response = mock.Mock()
        response.status_code = 404
        self.requests.get = mock.Mock(return_value=response)

        with self.assertRaises(Exception):
            self.client.get_job(_requests=self.requests)

    def test_do_job(self):
        self.requests.post = mock.Mock()
        do_action = mock.Mock(return_value={"ip": "127.0.0.1"})
        self.client.do_job("yyyy", "ping", {"ip": "127.0.0.1"}, _do_action=do_action, _requests=self.requests)


        self.requests.post.assert_called_with(
            'http://127.0.0.1:80/v1/node/job',
            json={
                'instantiated_job_id': 'yyyy', 
                'status': 'success', 
                'result': 
                    {
                        'ip': '127.0.0.1'
                    }
                }, 
            headers={'Authorization': 'Bearer xxxx'}
        )

    def test_do_job_failed(self):
        self.requests.post = mock.Mock()
        do_action = mock.Mock(side_effect=Exception("Ip range forbidden"))
        self.client.do_job("yyyy", "ping", {
                           "ip": "127.0.0.1"}, _do_action=do_action, _requests=self.requests)

        self.requests.post.assert_called_with(
            'http://127.0.0.1:80/v1/node/job',
            json = {'instantiated_job_id': 'yyyy', 'status': 'failed'}, 
            headers = {'Authorization': 'Bearer xxxx'}
        )

