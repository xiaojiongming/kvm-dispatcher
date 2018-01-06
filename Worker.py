import time
import json
import socket
import Tools

class Worker:
    def __init__(self):
        pass

    @staticmethod
    def heartbeatdealer(arg: dict):
        returnval = {}
        returnval['localtimestap'] = time.time()
        returnval['receivedtimestap'] = arg['timestap']
        returnval['ok'] = 'yes'
        return json.dumps(returnval).encode()

    @staticmethod
    def heartbeatconstuctor(remote: str, retry: int, arg: dict):
        client = socket.socket()
        client.settimeout(3)
        while retry > 0:
            try:
                client.connect(remote)
            except socket.timeout as e:
                print('connect to ' + str(remote) + ' timeout, remain retry ' + str(retry))
                retry = retry - 1
        if retry:
            client.send(Tools.jsontool.convertjson(func='heartbeat', arg=arg))
            receive = client.recv(8192)
            try:
                jsonobj = json.loads(receive)
                print(jsonobj)
            except Exception as e:
                print('invalid json received')
                print('receive from ' + str(client) + '::' + str(receive))
            finally:
                client.close()
        else:
            client.close()
            print('connect to ' + str(remote) + ' error,will handle nanresponse')

if __name__ == "__main__":
    pass
