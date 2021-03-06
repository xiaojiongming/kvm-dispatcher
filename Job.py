import socket
import ConfigReader
import time
import json
import Tools
import psutil
import logging

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
            job.doit()
        self.__jobq.clear()

    def addselfjob(self):
        pass

    def getjobq(self):
        return self.__jobq


class Heartbeat:
    def __init__(self, remote):
        self.remote = remote

    def doit(self):
        soc = Tools.socketbuilder(self.remote, 'heartbeat', {})
        logging.info('request to ' + self.remote + '::heartbeat')
        returnval = soc.buildsocketandsend()
        if returnval != {}:
            logging.info('get response ' + str(returnval))

    @staticmethod
    def heartbeathandle(args):
        returnval = {}
        returnval['localtimestap'] = time.time()
        returnval['receivedtimestap'] = args['timestap']
        returnval['ok'] = 'yes'
        return json.dumps(returnval).encode()

    @staticmethod
    def handlenonresponse(remote):
        '''
        plain: if non response happend , try any fence method or try acquire sanlock
                then update cluster info in share storage
        :return:
        '''
        logging.info('host::' + str(remote) + ' in non response , handle nonresponse')
        return 0

    def getremote(self):
        return self.remote


class Perf:
    def __init__(self, remote):
        self.perfconut = {}
        self.remote = remote
        self.perfconut['cpu'] = self.getcpuinfo()
        self.perfconut['mem'] = self.getmeminfo()
        self.perfconut['net'] = self.getnetinfo()
        self.perfconut['disk'] = self.getdiskinfo()

    def doit(self):
        soc = Tools.socketbuilder(self.remote, 'performance', {})
        logging.info('request to ' + self.remote + '::performance')
        returnval = soc.buildsocketandsend()
        if returnval != {}:
            logging.info('get response ' + str(returnval))

    def getcpuinfo(self):
        cpu = psutil.cpu_times()
        cpuinfo = {}
        cpuinfo['user'] = cpu.user
        cpuinfo['system'] = cpu.system
        cpuinfo['idle'] = cpu.idle
        cpuinfo['iowait'] = cpu.iowait
        return cpuinfo

    def getmeminfo(self):
        mem = psutil.virtual_memory()
        meminfo = {}
        meminfo['available'] = mem.available
        meminfo['percent'] = mem.percent
        meminfo['free'] = mem.free
        return meminfo

    def getnetinfo(self):
        '''
        {'lo': snetio(bytes_sent=1951120, bytes_recv=1951120, packets_sent=3579, packets_recv=3579, errin=0, errout=0,
        dropin=0, dropout=0), 'enp0s3': snetio(bytes_sent=825893, bytes_recv=10641052, packets_sent=7318,
         packets_recv=11008, errin=0, errout=0, dropin=0, dropout=0)}
        '''
        return psutil.net_io_counters(pernic=True)

    def getdiskinfo(self):
        '''
        {'sr0': sdiskio(read_count=0, write_count=0, read_bytes=0, write_bytes=0, read_time=0, write_time=0,
         read_merged_count=0, write_merged_count=0, busy_time=0), 'sda1': sdiskio(read_count=44840, write_count=9446,
         read_bytes=1292641280, write_bytes=607412224, read_time=67136, write_time=118664, read_merged_count=7319,
         write_merged_count=15834, busy_time=34544)}
        :return:
        :return:
        '''
        return psutil.disk_io_counters(perdisk=True)

    @staticmethod
    def perfhandle(args):
        returnval = {}
        perf = Perf(remote='')
        for key in perf.perfconut:
            returnval[key] = perf.perfconut[key]
        returnval['receivedtimestap'] = args['timestap']
        returnval['ok'] = 'yes'
        return Tools.jsontool.convertjson('PerformanceResponse', returnval)


class jobcheck:
    def __init__(self, q):
        self.jobwaitq = q

    def doit(self):
        return self.jobwaitq.get()
