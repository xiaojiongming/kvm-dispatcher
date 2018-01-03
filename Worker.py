import time
import json


class Worker:
    def __init__(self):
        pass

    @staticmethod
    def heartbeat(arg: dict):
        returnval = {}
        returnval['localtimestap'] = time.time()
        returnval['receivedtimestap'] = arg['timestap']
        returnval['ok'] = 'yes'
        return json.dumps(returnval).encode()


if __name__ == "__main__":
    pass
