import unittest
import unittest.mock as mock
import re

from node.nmap import Nmap

NMAP_EXAMPLE = """# Nmap 7.01 scan initiated Tue May 28 18:53:50 2019 as: nmap --top-ports 10 -oG output.txt -sV -A -T4 --version-all -d 37.59.37.5
# Ports scanned: TCP(10;21-23,25,80,110,139,443,445,3389) UDP(0;) SCTP(0;) PROTOCOLS(0;)
Host: 38.59.37.5 (ns398199.ip-38-59-37.eu)	Status: Up
Host: 38.59.37.5 (ns398199.ip-38-59-37.eu)	Ports: 21/closed/tcp//ftp///, 22/open/tcp//ssh//OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)/, 23/closed/tcp//telnet///, 25/filtered/tcp//smtp///, 80/closed/tcp//http///, 110/closed/tcp//pop3///, 139/closed/tcp//netbios-ssn///, 443/closed/tcp//https///, 445/filtered/tcp//microsoft-ds///, 3389/closed/tcp//ms-wbt-server///
# Nmap done at Tue May 28 18:53:53 2019 -- 1 IP address (1 host up) scanned in 3.13 secondss
"""

class TestNmap(unittest.TestCase):

    def setUp(self):
        self.nmap = Nmap()

    def test_is_up(self):
        result = self.nmap.is_up(NMAP_EXAMPLE, "38.59.37.5")

        self.assertTrue(result)

    def test_is_up_fail(self):
        result = self.nmap.is_up(NMAP_EXAMPLE, "127.0.0.1")

        self.assertFalse(result)

    def test_get_ip_dns_ports(self):

        result = self.nmap.get_ip_dns_ports(NMAP_EXAMPLE)
        expected = (
            "38.59.37.5",
            "ns398199.ip-38-59-37.eu",
            "21/closed/tcp//ftp///, 22/open/tcp//ssh//OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)/, 23/closed/tcp//telnet///, 25/filtered/tcp//smtp///, 80/closed/tcp//http///, 110/closed/tcp//pop3///, 139/closed/tcp//netbios-ssn///, 443/closed/tcp//https///, 445/filtered/tcp//microsoft-ds///, 3389/closed/tcp//ms-wbt-server///"
        )
        self.assertEqual(result, expected)

    def test_parse_ports(self):

        ports = "21/closed/tcp//ftp///, 22/open/tcp//ssh//OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)/, 23/closed/tcp//telnet///, 25/filtered/tcp//smtp///, 80/closed/tcp//http///, 110/closed/tcp//pop3///, 139/closed/tcp//netbios-ssn///, 443/closed/tcp//https///, 445/filtered/tcp//microsoft-ds///, 3389/closed/tcp//ms-wbt-server///"
        result = self.nmap.parse_ports(ports)
        expected = [
            {'port': '21', 'state': 'closed', 'protocol': 'tcp', 'service': 'ftp'}, 
            {'port': '22', 'state': 'open', 'protocol': 'tcp', 'service': 'ssh', 'version': 'OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)'}, 
            {'port': '23', 'state': 'closed', 'protocol': 'tcp', 'service': 'telnet'}, 
            {'port': '25', 'state': 'filtered', 'protocol': 'tcp', 'service': 'smtp'}, 
            {'port': '80', 'state': 'closed', 'protocol': 'tcp', 'service': 'http'}, 
            {'port': '110', 'state': 'closed', 'protocol': 'tcp', 'service': 'pop3'}, 
            {'port': '139', 'state': 'closed', 'protocol': 'tcp', 'service': 'netbios-ssn'}, 
            {'port': '443', 'state': 'closed', 'protocol': 'tcp', 'service': 'https'}, 
            {'port': '445', 'state': 'filtered', 'protocol': 'tcp', 'service': 'microsoft-ds'}, 
            {'port': '3389', 'state': 'closed', 'protocol': 'tcp', 'service': 'ms-wbt-server'}
        ]

        self.assertEqual(result, expected)

    def test_parse_nmap(self):
        result = self.nmap.parse_nmap(NMAP_EXAMPLE, "38.59.37.5")
        expected = {
            "status" : "up",
            "ip": "38.59.37.5",
            "dns": "ns398199.ip-38-59-37.eu",
            "scan": [
                {'port': '21', 'state': 'closed',
                    'protocol': 'tcp', 'service': 'ftp'},
                {'port': '22', 'state': 'open', 'protocol': 'tcp', 'service': 'ssh',
                    'version': 'OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)'},
                {'port': '23', 'state': 'closed',
                    'protocol': 'tcp', 'service': 'telnet'},
                {'port': '25', 'state': 'filtered',
                    'protocol': 'tcp', 'service': 'smtp'},
                {'port': '80', 'state': 'closed',
                    'protocol': 'tcp', 'service': 'http'},
                {'port': '110', 'state': 'closed',
                    'protocol': 'tcp', 'service': 'pop3'},
                {'port': '139', 'state': 'closed',
                    'protocol': 'tcp', 'service': 'netbios-ssn'},
                {'port': '443', 'state': 'closed',
                    'protocol': 'tcp', 'service': 'https'},
                {'port': '445', 'state': 'filtered',
                    'protocol': 'tcp', 'service': 'microsoft-ds'},
                {'port': '3389', 'state': 'closed',
                    'protocol': 'tcp', 'service': 'ms-wbt-server'}
            ]
        }

        self.assertEqual(result, expected)

    
