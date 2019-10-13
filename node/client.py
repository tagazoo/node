from time import sleep
import logging

import requests

from node.actions import do_action

class Client:
    def __init__(self, token:object, domain:str, scheme:str):
        # token : the bearer tokenbearer
        # domain : ip:port or domain
        # scheme : "http" or "https"

        self._token = token
        self._address = "{}://{}".format(scheme, domain)
        self._uri = self._address + "/v1/node/job"
        self._log = logging.getLogger("Client_" + str(id(self)))

    def _headers(self):
        token = str(self._token)
        return {"Authorization": "Bearer {}".format(token)}

    def main_loop(self, _sleep=sleep, _loop_condition=True):
        # process continiously

        while _loop_condition:
            _sleep(1)

            try:
                instantiated_job_id, action, parameters = self.get_job()
            except Exception as e:
                continue

            self._log.info("Do {} with parameters {}".format(action, parameters))

            self.do_job(instantiated_job_id, action, parameters, None)


    def get_job(self, _requests=requests)->tuple:
        # return instantiated_job_id, action and parameters
        # raise Exception on fail
        response = _requests.get(self._uri, headers=self._headers())

        if response.status_code != 200:
            if response.status_code == 400: # should not be 401 ?!
                self._log.error("Bad token")
                raise Exception("Bad token")

            self._log.debug("No job to do (status code : {})".format(response.status_code))
            raise Exception("Bad status code ({})".format(response.status_code))

        payload = response.json()

        return payload["instantiated_job_id"], payload["action"], payload["parameters"]

    def do_job(self, instantiated_job_id: str, action: str, parameters: dict, _do_action=None, _requests=requests)->dict:

        if not _do_action:
            _do_action = do_action

        try:
            result = _do_action(action, parameters)
        except Exception as e:
            self._log.info("Failed to run job ({})".format(e))
            response = {
                "instantiated_job_id" : instantiated_job_id,
                "status": "failed"
            }
            _requests.post(self._uri, json=response, headers=self._headers())
            return

        response = {
            "instantiated_job_id": instantiated_job_id,
            "status": "success",
            "result": result
        }
        _requests.post(self._uri, json=response, headers=self._headers())

    def is_server_up(self, _requests=requests):
        try:
            response = _requests.get(self._address+"/")
            if response.status_code != 200:
                raise Exception("Server status is invalid")

            return True
        except Exception as e:
            self._log.error("The server at {} is down".format(self._address))
            
        return False
        


