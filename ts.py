import socketserver
import queue
import threading
import json


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
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        self.add(testfunc.doit)

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
        # while True:
        print(self.request.recv(8192))
            # self.queue.put(self.request.recv(8192))
            # return json.dumps('{\'ok\':\'123\'}')
        self.request.send(str.encode(json.dumps('{\'ok\':\'true\'}')))

    def add(self, func):
        self._functions[func.__name__] = func


class testfunc:
    def __init__(self, *args, **kwargs):
        pass

    def doit(self, *args, **kwargs):
        return kwargs


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
    threading.Thread(target=getq, args=(q,)).start()
    server = ThreadedTCPStreamServer(('0.0.0.0', 8081), ThreadedTCPStreamHandler, queue=q)
    ip, port = server.server_address
    NWORKERS = 16
    for i in range(NWORKERS):
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
    server.serve_forever()
