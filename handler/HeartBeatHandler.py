
class HeartBeatHandler:
    def __init__(self, ):
        pass

    def do(self, *args):
        parameter = args[0]
        if 'jobid' in parameter and 'timestap' in parameter:
            return parameter['jobid'], parameter['timestap']
        else:
            return -1, -1