import subprocess
import logging
import re

HOST_RE = re.compile(r"Host: (\d+\.\d+\.\d+\.\d+) \(([\w\d\.-]*)\)\s+Ports: (.+)")
PORT_RE = re.compile(r"(\d+?)\/(\w*?)\/(\w+?)\/(.*?)\/(.*?)\/(.*?)\/(.*?)\/(.*)")
PORT_KEYS = ("port", "state", "protocol", "owner", "service", "rpc_info", "version")

class Nmap:
    def __init__(self):
        pass

    def __call__(self, parameters, _nmap_command=None):

        if not _nmap_command:
            _nmap_command = self.nmap_command

        ip = parameters["ip"]
        stdout = _nmap_command(ip)
        result = self.parse_nmap(stdout, ip)

        return result

    def nmap_command(self, ip:str):

        output = subprocess.run(
            ["nmap", "--top-ports", "100", "-oG", "-", "-sV", "-A", "--version-all", "-d", ip], stdout=subprocess.PIPE)
        stdout = str(output.stdout, "utf8")
        return stdout

    def is_up(self, stdout, ip):

        if re.search("Host: {}.+?Status: (Up|Unknow)".format(ip), stdout):
            return True
        return False

    def get_ip_dns_ports(self, stdout):
        # from greppable nmap output
        # extract the ip, the dns and ports
        # ports need to be extract one by one
        re_result = HOST_RE.search(stdout)
        return re_result.groups()

    def parse_ports(self, ports):
        # format is ($port, $state, $protocol, $owner, $service, $rpc_info, $version)
        output = []
        for p in ports.split(", "):
            splitted = zip(PORT_KEYS, PORT_RE.search(p).groups())
            only_available_field = filter(lambda x: len(x[1])>0, splitted)
            port_info = dict(only_available_field)
            output.append(port_info)

        return output

    def parse_nmap(self, stdout, ip):

        if not self.is_up(stdout, ip):
            return {"ip":ip, "status":"down"}
        
        output = {"ip": ip, "status": "up"}

        _, dns, ports = self.get_ip_dns_ports(stdout)
        output["dns"] = dns
        output["scan"] = self.parse_ports(ports)

        return output

            
