import unittest
import unittest.mock as mock
import re

from node.ping import Ping

PING_OK_EXAMPLE = 'PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.\n64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.037 ms\n64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.020 ms\n64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.066 ms\n\n--- 127.0.0.1 ping statistics ---\n3 packets transmitted, 3 received, 0% packet loss, time 1998ms\nrtt min/avg/max/mdev = 0.020/0.041/0.066/0.019 ms\n'
PING_KO_EXAMPLE = 'PING 10.0.0.1 (10.0.0.1) 56(84) bytes of data.\n\n--- 10.0.0.1 ping statistics ---\n3 packets transmitted, 0 received, 100% packet loss, time 2016ms\n\n'

class TestPing(unittest.TestCase):

    def setUp(self):
        self.ping = Ping()

    # def test_ping_command(self):
    #     self.ping.ping_command("127.0.0.1")

    # def test_ping_command_failed(self):
    #     print(self.ping.ping_command("10.0.0.1"))

    def test_get_ttl_and_time(self):
        result = self.ping.get_ttl_and_time(PING_OK_EXAMPLE)
        expected = ([64, 64, 64], [0.037, 0.020, 0.066])

        self.assertEqual(result, expected)

    def test_get_ttl_and_time_failed(self):
        result = self.ping.get_ttl_and_time(PING_KO_EXAMPLE)
        expected = ([],[])

        self.assertEqual(result, expected)

    def test_get_statistics(self):
        result = self.ping.get_scan_statistics(PING_OK_EXAMPLE)
        expected = (3, 3, 1998)
        self.assertEqual(result, expected)

    def test_call(self):
        ping_command = mock.Mock(return_value=PING_OK_EXAMPLE)
        parameters = {"ip":"127.0.0.1"}
        result = self.ping(parameters, ping_command)
        expected = {
            'packet_transmitted': 3, 
            'packet_received': 3,
            'scan_time': 1998, 
            'ttl': [64, 64, 64], 
            'time': [0.037, 0.02, 0.066]
        }
        self.assertEqual(result, expected)


    
