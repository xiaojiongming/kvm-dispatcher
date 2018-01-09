import Job
import Listener
import threading
import queue
import time
import ConfigReader
import os
import socket
import Tools
import sys


class ENVChecker:
    def __init__(self, config):
        '''
        plain : check all environment status include network/storage/libvirt etc
        if everything seems ok, then start Listener and timer job.
        '''
        self.__config = config
        self.__tools = Tools.globalinfotool()
        self.checkall()
        self.hostlist = []
        self.ipaddress = ''


    def checkall(self):
        if not (self.checkstorage() and self.checknetwork()):
            return 0

    def checkstorage(self):
        '''
        plain: try to mount share storage and test some io in it.
               then try test sanlock, if ok return 0
        :return:
        '''
        if os.path.isdir('/storage/storageinfo'):
            if os.path.isfile('/storage/globalmeta'):
                return 0
        return 1

    def checknetwork(self):
        '''
        plain : check network status , include:
            1.any ip can be use?
            2.can connect to other host?
        :return:
        '''
        listenport = self.__config.getbykey('port', 'main')
        testbind = socket.socket()
        try:
            testbind.bind(('0.0.0.0', self.__config.getbykey('port', 'main')))
        except OSError as e:
            print('port ' + str(listenport) + ' already in use')
            if self.__config.getbykey('debug', 'main') == 'on':
                print('DEBUG::' + str(e))
            return -1
        finally:
            testbind.close()

        self.__hostlist = self.__tools.getallhost()
        if self.__config.getbykey('debug', 'main') == 'on':
            print('DEBUG::get host list ' + str(self.__hostlist) + ' from global meta ,will send heart beat')
        return 0

    def checksanlock(self):
        '''
        plain: check if sanlock can work properly, then add local to sanlock lockspace
               need sanlock tools to collab this.
        return sanlock instance
        :return:
        '''
        pass


class start:
    def __init__(self):
        self.__config = ConfigReader.ConfigReader('./main.cfg')
        self.__envchecker = ENVChecker(self.__config)

        if self.__envchecker.checkall() == 0:
            self.__envchecker.checksanlock()
            self.__globalq = queue.Queue()
            self.__jobwaitq = queue.Queue()
        else:
            print('some thing error ,trace log')
            sys.exit(-1)

    def startlistenerandjober(self):
        '''
        prepare a queue for threads communication
        :return:
        '''
        listener = Listener.startlistener(self.__globalq)
        threading.Thread(target=listener.start).start()
        threading.Thread(target=self.addheartbeatjobtoq).start()
        threading.Thread(target=self.starttimerjob, args=(self.__jobwaitq,)).start()

    def starttimerjob(self, jobwaitq: queue.Queue):
        jober = Job.jober()
        while True:
            jobwaitq.put(jober.getjobq())
            job = self.__globalq.get()
            jober.addjob(job)
            jober.executejob()
            time.sleep(int(self.__config.getbykey('jobsleep', 'jober')))

    def addheartbeatjobtoq(self):
        pollinginterval = self.__config.getbykey('interval', 'heartbeat')
        while True:
            tools = Tools.globalinfotool()
            for host in iter(tools.getallhost()):
                heartbeatjob = Job.Heartbeat(host)
                self.__globalq.put(int(heartbeatjob))
            time.sleep(pollinginterval)


if __name__ == '__main__':
    s = start()
    s.startlistenerandjober()
