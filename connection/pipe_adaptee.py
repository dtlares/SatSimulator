""" pipe adaptee"""
from connection.i_net_adaptee import INetAdaptee


class PipeAdaptee(INetAdaptee):
    """ pipe adaptee"""
    def has_data(self) -> bool:
        """ Returns true if the adapter received data  """
        return self.conn.poll()

    def send(self, data):
        """ Sends the data  """
        self.conn.send(data)

    def recv(self):
        """ Reads the data  """
        return self.conn.recv()
