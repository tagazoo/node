import subprocess
import logging
import re

RE_TTL_AND_TIME = re.compile(r"icmp_seq=\d+ ttl=(\d+) time=([\d+\.]+)")
RE_STATISTICS = re.compile(r"(\d+) packets transmitted, (\d+) received,.+?time (\d+)")

class Ping:
    def __init__(self):
        pass

    def __call__(self, parameters, _ping_command=None):

        if not _ping_command:
            _ping_command = self.ping_command

        ip = parameters["ip"]
        stdout = _ping_command(ip)
        ttl, time = self.get_ttl_and_time(stdout)
        transmitted, received, scan_time = self.get_scan_statistics(stdout)

        result = {
            "packet_transmitted": transmitted,
            "packet_received": received,
            "scan_time": scan_time,
            "ttl": ttl,
            "time": time
        }

        return result

    def ping_command(self, ip:str):

        output = subprocess.run(["ping", "-c", "3", ip], stdout=subprocess.PIPE)
        stdout = str(output.stdout, "utf8")
        return stdout

    def get_ttl_and_time(self, stdout):
        re_output = RE_TTL_AND_TIME.findall(stdout)
        
        ttl = list(map(lambda x: int(x[0]), re_output))
        time = list(map(lambda x: float(x[1]), re_output))

        return ttl, time

    def get_scan_statistics(self, sdtout):
        re_output = RE_STATISTICS.search(sdtout)
        return tuple(map(int, re_output.groups()))
