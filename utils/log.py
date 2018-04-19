""" Tools for logging"""
import inspect


class MsgType:
    """ Different colors for the console"""
    HEADER = '\033[95m'
    INFO = '\033[94m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Log:
    """ Logging Utility"""
    suppress_log = False

    @staticmethod
    def log(msg_type: MsgType, action: str, msg: str):
        """ Logging function"""
        if not Log.suppress_log:
            print("%s %s - %s - %s " % (msg_type, inspect.stack()[1][3], action, msg))
