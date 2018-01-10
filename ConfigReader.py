import configparser
import os


class ConfigReader:
    def __init__(self, configpath):
        self.__cfp = configparser.ConfigParser()
        if os.path.isfile(configpath):
            self.__cfp.read(configpath)

    def getbykey(self, key, section=''):
        if self.__cfp.has_option(section, key):
            return self.__cfp.get(section=section,option=key)
        else:
            return -1, 'no such key'


if __name__ == '__main__':
    c = ConfigReader('./main.cfg')
    c.getbykey('worker', 'main')
