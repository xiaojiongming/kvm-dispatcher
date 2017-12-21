import threading
import queue


class WorkerPool:
    def __init__(self, workercount):
        self.__globalq = queue.Queue(workercount)
        self.__globaljoblock = threading.Lock()



class Worker(threading.Thread):
    pass

if __name__ == "__main__":
    pass
