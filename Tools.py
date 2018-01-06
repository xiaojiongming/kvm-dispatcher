import ConfigReader
import socket
import time
import json


class globalinfotool:
    def __init__(self):
        self.__config = ConfigReader.ConfigReader('/storage/storageinfo/globalmeta')

    def getallhost(self):
        return self.__config.getbykey('hosts', 'hostlist').split(';').remove(self.getselfipaddr())

    @staticmethod
    def getselfipaddr():
        return socket.gethostbyname(socket.gethostname())


class jsontool:

    @staticmethod
    def convertjson(func, arg):
        returndict = {}
        returndict['timestap'] = time.time()
        returndict['function'] = func
        for key in arg:
            returndict[key] = arg[key]
        return json.dumps(returndict).encode()
