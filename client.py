import socket
import time
import json
import threading

def client(*ip):
    def convertjson(func, arg):
        returndict = {}
        returndict['timestap'] = time.time()
        returndict['function'] = func
        for key in arg:
            returndict[key] = arg[key]
        return json.dumps(returndict).encode()

    client = socket.socket()
    client.connect(ip)
    args = {'testk': 'testv'}
    client.send(convertjson(func='heartbeat', arg=args))
    receive = client.recv(8192)
    try:
        jsonobj = json.loads(receive)
        print(jsonobj)
    except Exception as e:
        print('invalid json received')
        print('receive from ' + str(client) + '::' + str(receive))
    finally:
        client.close()


for i in range(50):
    threading.Thread(target=client, args=(('localhost', 8082))).start()