"""This module includes the Command Abstract class"""
import abc
import functools
from datetime import datetime
from enum import Enum, auto


class Command(metaclass=abc.ABCMeta):
    """Command Abstract class"""
    error_threshold = 1

    class Status(Enum):
        """Command Status"""
        not_executed = auto()
        executed = auto()
        in_progress = auto()
        failed = auto()

    def set_timestamp(func):
        """Time stamp decorator - sets the timestamp when the command is executed"""
        functools.wraps(func)

        def inner(*args):
            """ Decorator """
            args[0].time_stamp = datetime.now()
            return func

        return inner

    def __init__(self, cmd_id: int, cmd_type: str, source: str, dest: str, param: list, execute_at: int = -1,
                 time_stamp: int = -1, status: Status = Status.not_executed, payload=None, payoff=0):
        """Command constructor.
            cmd_id: the command id
            cmd_type: the type of the command
            source: the source of the command
            dest: the destination of the command
            param: the execution parameters
            execute_at: the time that the command should be executed
            time_stamp: the execution time
            status: the status of the command - planned, executed
        """
        self.cmd_id = cmd_id
        self.source = source
        self.dest = dest
        self.time_stamp = time_stamp
        self.cmd_type = cmd_type
        self.param = param
        self.execute_at = execute_at
        self.status = status
        self.payload = payload
        self.payoff = payoff

    @abc.abstractmethod
    def execute_command(self):
        """Abstract Execute a command"""
        pass

    def __str__(self):
        """String representation of a Command"""
        string = 'Id: %s, Type: %s, ' % (str(self.cmd_id), self.cmd_type)
        string += ' Src: %s, Dest: %s, ' % (self.source, self.dest)
        string += 'Execute at: %s, Time Stamp: %s, ' % (self.execute_at, self.time_stamp)
        string += 'Status: %s' % self.status
        return string
