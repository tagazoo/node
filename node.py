import logging

from docopt import docopt

from node.client import Client
from node.token import Token

cli_doc = """Tagazoo node

Usage:
  node.py -a=<domain> [-s=<scheme>] 
  node.py (-h | --help)
  node.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  -a=<domain>   Target domain [default: api.tagazoo.com].
  -s=<scheme>   Type of scheme [default: https]
"""

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    arguments = docopt(cli_doc, version='Node v1')
    token = Token()
    token.load_token()
    domain = arguments["-a"]
    scheme = arguments["-s"]
    client = Client(token, domain, scheme)

    if client.is_server_up():
      client.main_loop()
