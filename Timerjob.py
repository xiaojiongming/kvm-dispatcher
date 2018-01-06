import socket
import ConfigReader


class jober:
    def __init__(self):
        '''
        plain: global job queue
        '''
        self.__jobq = []

    def addjob(self, job):
        self.__jobq.append(job)

    def executejob(self):
        for job in self.__jobq:
            pass

    def addselfjob(self):
        pass


class Heartbeatchecker:
    def __init__(self, remote):
        self.__config = ConfigReader.ConfigReader('./main.cfg')
        self.remotehost = remote
        self.__connectiontimeout = self.__config.getbykey('timeout', 'heartbeat')
        self.__retry = int(self.__config.getbykey('retry', 'heartbeat'))

    def send(self):
        if self.__retry != 0:
            client = socket.socket()
            client.timeout = self.__connectiontimeout
            try:
                client.connect(self.remotehost)
            except socket.timeout as e:
                self.__retry = self.__retry - 1
                print('connect to ' + str(self.remotehost) + ' timeout[' + str(
                    self.__connectiontimeout) + '] remain retry:' + str(self.__retry))
        else:
            self.handlenonresponse()

    def handlenonresponse(self):
        '''
        plain: if non response happend , try any fence method or try acquire sanlock
                then update cluster info in share storage
        :return:
        '''
        pass
