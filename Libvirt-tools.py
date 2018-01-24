import libvirt
import logging
import traceback
import sys


class libvirttool:
    def __init__(self):
        try:
            self.__conntion = libvirt.open("qemu:///system")
        except libvirt.libvirtError as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.ERROR("can not connect to local libvirt daemon" + repr(
                traceback.format_tb(traceback.format_tb(exc_traceback))))

    def getconnection(self):
        return self.__conntion

    def getvmlist(self):
        self.__conntion.getAllDomainStats()
