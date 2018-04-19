""" This module has classes to represent a message"""
from enum import Enum, auto


class Message:
    """ Message class"""

    class MsgType(Enum):
        """ Types of messages. ack and executed are triggered and received internally by the
        adapters."""
        ack = auto()
        status = auto()
        command = auto()
        no_ack = auto()
        executed = auto()

    def __init__(self, msg_type: MsgType, msg_id: int, source: str, destination: str, data=None):
        """ Message constructor
        msg_type: the type of the message
        source: the origin of the message
        destination: the destination of the message
        data: the message information, usually a packed data"""
        self.msg_type = msg_type
        self.msg_id = msg_id
        self.destination = destination
        self.source = source
        self.data = data

    def __str__(self):
        """ String representation of the Message """
        msg_id = str(self.msg_id)
        return "[%s] - %s Message from %s to %s " % (msg_id, self.msg_type, self.source, self.destination)
