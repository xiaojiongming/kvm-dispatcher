import jsonrpcserver
import simpleworker
import ConfigReader

class RPCServer():
    def __init__(self, config):
        self.__handler = [simpleworker.testclass]
        self.__serverport = int(config.getbykey('port', 'main'))

    def serverstart(self):
        jsonrpcserver.methods.serve_forever(port=self.__serverport)

    def registehandle(self):
        for worker in self.__handler:
            handler = worker()
            jsonrpcserver.methods.add_method(handler.result)


if __name__ == '__main__':
    config = ConfigReader.ConfigReader('./main.cfg')
    R = RPCServer(config)
    R.registehandle()
    R.serverstart()

