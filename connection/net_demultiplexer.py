""" This is a demultiplexer. It has similar interface than the net adapter.
    It is used to deliver messages to different adapters."""
from .msg_pkg import Message
from .net_adapter import NetAdapter


class DeMultiplexer:
    """De multiplexes messages to different adapters"""
    def __init__(self, callback=None):
        """C onstructor """
        self._connections = {}
        self._callback = callback

    def __call__(self, msg: Message):
        """ Sends a message"""
        self.send(msg)

    def connection_exists(self, conn_name: str) -> bool:
        """ Returns true if the multiplexer is connected to a particular adapter."""
        return self._connections.get(conn_name) is not None

    def add_connection(self, conn_name: str, net_adapter: NetAdapter) -> bool:
        """ Adds a new connection to an adapter"""
        if not self.connection_exists(conn_name):
            self._connections[conn_name] = net_adapter
            return True

        return False

    def remove_connection(self, conn_name: str):
        """ Removes the adapter """
        self._connections.pop(conn_name, None)

    def send(self, msg: Message) -> bool:
        """ Sends a message """
        if self.connection_exists(msg.destination):
            self._connections[msg.destination].send(msg)
            return True
        return False

    def receive(self, data):
        """ Receives a message """
        self._callback(data)
