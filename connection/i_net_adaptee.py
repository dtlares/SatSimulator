""" This module contains an abstract class """
import abc


class INetAdaptee(metaclass=abc.ABCMeta):
    """ Abstract Class  """

    def __init__(self, conn):
        """ Constructor  """
        self.conn = conn

    @abc.abstractmethod
    def has_data(self) -> bool:
        """ Returns true if the adapter received data  """
        pass

    @abc.abstractmethod
    def send(self, data):
        """ Sends the data  """
        pass

    @abc.abstractmethod
    def recv(self):
        """ Reads the data  """
        pass
