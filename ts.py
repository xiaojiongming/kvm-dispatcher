import socketserver
import queue
import threading
import json
import socket
import time
from Worker import Worker
import ConfigReader

class ThreadedTCPStreamServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True,
                 queue=None):
        self.queue = queue
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass,
                                        bind_and_activate=bind_and_activate)


class ThreadedTCPStreamHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.queue = server.queue
        self._functions = {}
        self.add(Worker.heartbeat)
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)

    # def handle(self):
    #     while True:
    #         func_name, args, kwargs = json.loads(self.request.recv(8192))
    #         # msg = self.request.recv(8192)
    #         try:
    #             r = self._functions[func_name](*args, **kwargs)
    #             self.request.send(json.dumps(r))
    #         except Exception as e:
    #             self.request.send(json.dumps(str(e)))
    #
    #         # self.queue.put(msg)
    #         # self.finish()

    def handle(self):

        jsonobj = self.request.recv(8192)
        responsedict = {}
        requestdict = {}
        config = ConfigReader.ConfigReader('./main.cfg')
        if config.getbykey('debug', 'main') == 'on':
            print('recevied json from ' + str(self.client_address) + '::' + str(jsonobj))
        try:
            requestdict = json.loads(jsonobj)
        except json.decoder.JSONDecodeError as e:
            print('invalid json' + str(e))
            responsedict['ok'] = 'no'
            responsedict['localtimestap'] = time.time()
            self.request.send(json.dumps(responsedict).encode())

        if requestdict != {}:
            if requestdict.__contains__('function'):
                func = requestdict['function']
                executed = self._functions[func](requestdict)
                if config.getbykey('debug', 'main') == 'on':
                    print('sendback json to ' + str(self.client_address) + '::' + str(executed))
                self.request.send(executed)




    def add(self, func):
        self._functions[func.__name__] = func



if __name__ == '__main__':
    def getq(q: queue.Queue):
        while True:
            try:
                print('start get')
                item = q.get()
                print(item)
                q.task_done()
                q.join()
            except Exception:
                server.shutdown()


    q = queue.Queue()
    # threading.Thread(target=getq, args=(q,)).start()
    server = ThreadedTCPStreamServer(('0.0.0.0', 8082), ThreadedTCPStreamHandler, queue=q)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()


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
        except Exception as e:
            print('invalid json received')


    for i in range(2):
        time.sleep(0.5)
        threading.Thread(target=client, args=(('localhost', 8082))).start()
