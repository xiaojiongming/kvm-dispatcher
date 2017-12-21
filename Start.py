from jsonrpcserver import methods
import Worker
import threading


@methods.add
def handlerequest(fun,args):

    return