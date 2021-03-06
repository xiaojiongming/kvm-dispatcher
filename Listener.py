import socketserver
import queue
import json
import time
import ConfigReader
import Job
import traceback
import logging


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
        self.add('heartbeat', Job.Heartbeat.heartbeathandle)
        self.add('performance', Job.Perf.perfhandle)
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
        try:
            requestdict = json.loads(jsonobj)
            logging.info('get request from ' + str(self.client_address) + '::' + str(requestdict))
        except json.decoder.JSONDecodeError as e:
            logging.error('invalid json' +
                          str(e))
            responsedict['ok'] = 'no'
            responsedict['localtimestap'] = time.time()
            self.request.send(json.dumps(responsedict).encode())

        if requestdict != {}:
            if requestdict.__contains__('function'):
                func = requestdict['function']
                executed = self._functions[func](requestdict)
                logging.debug('response to ' + str(self.client_address) + '::' + str(executed))
                self.request.send(executed)

    def add(self, funcname, func):
        self._functions[funcname] = func


class startlistener:
    def __init__(self, globalq):
        config = ConfigReader.ConfigReader('./main.cfg')
        locallisten = config.getbykey('ip', 'main'), int(config.getbykey('port', 'main'))
        self.__server = ThreadedTCPStreamServer(locallisten, ThreadedTCPStreamHandler, queue=globalq)

    def start(self):
        self.__server.serve_forever()


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
    server.serve_forever()

    # server_thread = threading.Thread(target=server.serve_forever)
    # server_thread.daemon = True
    # server_thread.start()
