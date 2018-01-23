import ConfigReader
import socket
import time
import json
import Job
import logging
import traceback
import sys

class globalinfotool:
    def __init__(self):
        self.__config = ConfigReader.ConfigReader('/storage/storageinfo/globalmeta')

    def getallhost(self):
        hostlist = self.__config.getbykey('hosts', 'global').split(';')
        selfip = hostlist.remove(self.getselfipaddr())
        for k, ip in enumerate(hostlist):
            if ip == selfip:
                hostlist.remove(k + 1)
        return hostlist

    @staticmethod
    def getselfipaddr():
        return socket.gethostbyname(socket.gethostname())


class jsontool:
    @staticmethod
    def convertjson(func, data):
        returndict = {}
        returndict['timestap'] = time.time()
        returndict['function'] = func
        if data:
            for key in data:
                returndict[key] = data[key]
        return json.dumps(returndict).encode()


class socketbuilder:
    def __init__(self, remote, func, dictdata):
        self.__config = ConfigReader.ConfigReader('./main.cfg')
        self.__remotehost = remote
        self.__connectiontimeout = int(self.__config.getbykey('timeout', 'heartbeat'))
        self.__retry = int(self.__config.getbykey('retry', 'heartbeat'))
        self.__port = int(self.__config.getbykey('port', 'main'))
        self.targetfunc = func
        self.__data = dictdata

    def buildsocketandsend(self):
        while self.__retry != 0:
            self.client = socket.socket()
            self.client.settimeout(self.__connectiontimeout)
            try:
                self.client.connect((self.__remotehost, self.__port))
                self.client.send(jsontool.convertjson(self.targetfunc, self.__data))
                receive = self.client.recv(8192)
                try:
                    jsonobj = json.loads(receive.decode())
                    return jsonobj
                except Exception as e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    logging.error('invalid json received receive from ' + str(self.client.getpeername()) + '::' + repr(
                        traceback.format_tb(exc_traceback)))
                    return {}
            except socket.timeout as e:
                self.__retry = self.__retry - 1
                logging.error('connect to ' + str(self.__remotehost) + ' timeout[' + str(
                    self.__connectiontimeout) + '] remain retry:' + str(self.__retry))
            except OSError as e:
                self.__retry = self.__retry - 1
                logging.error(
                    'connect to ' + str(self.__remotehost) + ' with error::' + str(e) + ' remain retry:' + str(
                    self.__retry))
            finally:
                self.client.close()
                time.sleep(2)
        Job.Heartbeat.handlenonresponse(self.__remotehost)

