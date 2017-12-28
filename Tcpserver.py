import socketserver
import queue
import threading


class ThreadedTCPStreamServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True,
                 queue=None):
        self.queue = queue
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass,
                                        bind_and_activate=bind_and_activate)


class ThreadedTCPStreamHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.queue = server.queue
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        while True:
            msg = self.request.recv(8192)
            if not msg:
                break
            self.queue.put(msg)
            self.request.send(msg)
            self.finish()


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
