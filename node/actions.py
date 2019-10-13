from node.ping import Ping
from node.nmap import Nmap


ACTIONS = {
    "ping" : Ping(),
    "nmap" : Nmap()
}

def do_action(action, parameters):

    if action not in ACTIONS:
        raise NotImplementedError(action)

    return ACTIONS[action](parameters)