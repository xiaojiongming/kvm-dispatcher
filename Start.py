import Timerjob
import Listener
import threading
import queue
import time
import ConfigReader


class ENVChecker:
    def __init__(self):
        '''
        plain : check all environment status include network/storage/libvirt etc
        if everything seems ok, then start Listener and timer job.
        '''
        self.checkall()

    def checkall(self):
        if not (self.checkstorage() and self.checknetwork()):
            return 0

    def checkstorage(self):
        '''
        plain: try to mount share storage and test some io in it.
               then try test sanlock, if ok return 0
        :return:
        '''
        return 0

    def checknetwork(self):
        '''
        plain : check network status , include:
            1.any ip can be use?
            2.can connect to other host?
        :return:
        '''
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
        envchecker = ENVChecker()
        if envchecker.checkall() == 0:
            envchecker.checksanlock()
            self.__globalq = queue.Queue()

    def startlistenerandjober(self):
        '''
        prepare a queue for threads communication
        :return:
        '''
        listener = Listener.startlistener(self.__globalq)
        threading.Thread(target=listener.start).start()
        threading.Thread(target=self.starttimerjob).start()

    def starttimerjob(self):
        jober = Timerjob.jober()
        while True:
            job = self.__globalq.get()
            jober.addjob(jober)
            jober.executejob()
            time.sleep(int(self.__config.getbykey('jobsleep', 'jober')))


if __name__ == '__main__':
    s = start()
    s.startlistenerandjober()
