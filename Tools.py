import ConfigReader
import socket
import time
import json


class globalinfotool:
    def __init__(self):
        self.__config = ConfigReader.ConfigReader('/storage/storageinfo/globalmeta')

    def getallhost(self):
        hostlist = self.__config.getbykey('hosts', 'global').split(';')
        selfip = hostlist.remove(self.getselfipaddr())
        for k, ip in enumerate(hostlist):
            if ip == selfip:
                hostlist.remove(k+1)
        return hostlist

    @staticmethod
    def getselfipaddr():
        return socket.gethostbyname(socket.gethostname())



class jsontool:

    @staticmethod
    def convertjson(func, **kwargs):
        returndict = {}
        returndict['timestap'] = time.time()
        returndict['function'] = func
        if kwargs:
            for key in kwargs:
                returndict[key] = kwargs[key]
        return json.dumps(returndict).encode()
