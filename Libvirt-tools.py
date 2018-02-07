import libvirt
import logging
import traceback
import sys


class libvirttool:
    def __init__(self, connectionuri="qemu:///system"):
        try:
            self.__conntion = libvirt.open(connectionuri)
        except libvirt.libvirtError as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.ERROR("can not connect to local libvirt daemon" + repr(
                traceback.format_tb(traceback.format_tb(exc_traceback))))

    def getconnection(self):
        return self.__conntion

    def getvmlist(self):
        vmdict = {}
        for vm in self.__conntion.listAllDomains():
            vmdict[vm.ID()] = vm.name()
        return vmdict

    def getcomp(self):
        return self.__conntion.getCapabilities()


if __name__ == "__main__":
    virtcontrole = libvirttool("qemu+tcp://minie@10.66.192.60:16510/system")
    print(virtcontrole.getvmlist())
