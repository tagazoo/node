import re

JWT_RE = re.compile(r"^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$")

class Token:
    def __init__(self, filename="/token/token"):
        self._filename = filename
        self._token = None

    def _read_token(self)->str:
        try:
            with open(self._filename) as f:
                return f.read()
        except Exception as e:
            print("No token file readable !")
            raise e

    def validate(self, token:str)->None:
        if not JWT_RE.match(token):
            raise Exception("JWT token is invalid")

    def load_token(self, _read_token=None)->None:
        # load a token for the file and validate it
        if _read_token is None:
            _read_token = self._read_token

        token = _read_token()
        self.validate(token)
        self._token = token

    def __str__(self)->str:
        return self._token


    

    

    
