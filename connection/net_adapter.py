""" This module contains the Network adapter class"""
import time
from threading import Thread
from utils.log import Log, MsgType
from connection.pipe_adaptee import PipeAdaptee
from connection.msg_pkg import Message


class NetAdapter:
    """ Network adapter class - Sends and receives information using different
        adaptee classes. Responds messages using callbacks"""
    def __init__(self, destination: str, conn_obj, callback_func, timeout=0.5):
        """ Constructor
            destination: the destination of the connection
            conn_obj: the connection chain
            callback_func: the function that is executed when a message is received
            timeout: the ack timeout
        """
        self._adaptee = PipeAdaptee(conn_obj)
        self._destination = destination
        self._timeout = timeout
        self._validation = {}
        self._callback_func = callback_func
        self._thread = Thread(target=self._recv)
        self._thread.start()

    def get_destination(self):
        """ Returns the destination of the connection """
        return self._destination

    def send(self, msg: Message):
        """ Sends a message """
        if msg.destination == self._destination:
            self._validation[str(msg.msg_id)] = {"sent_at": time.time(), "source": msg.source}
            Log.log(MsgType.INFO, "Adapter - Send", msg)
            self._adaptee.send(msg)
        else:
            raise ValueError("Wrong destination")

    def __call__(self, msg: Message):
        """Sends a message"""
        self.send(msg)

    def _cleanup_unresponded_msgs(self):
        """ Cleans all messages that were not responded on time """
        msg_to_delete = []
        current_time = time.time()

        for msg_id in self._validation:
            elapsed_time = current_time - self._validation[msg_id]["sent_at"]

            if elapsed_time > self._timeout:
                msg = Message(msg_type=Message.MsgType.no_ack, msg_id=msg_id,
                              destination=self._validation[msg_id]["source"],
                              source=self._destination)

                Log.log(MsgType.FAIL, "Adapter - NO-ACK", msg)
                msg_to_delete.append(msg_id)

        for msg_id in msg_to_delete:
            m = self._validation.pop(str(msg_id), None)
            del m

    def _remove_ack_msg(self, msg: Message):
        """ Removes the ack message """
        Log.log(MsgType.SUCCESS, "Adapter - ACK", msg)
        m = self._validation.pop(str(msg.msg_id), None)
        del m

    def _send_ack(self, msg: Message):
        """ Sends the ack message """
        Log.log(MsgType.INFO, "Adapter - Sending ACK", msg)
        self._adaptee.send(Message(msg_type=Message.MsgType.ack, msg_id=msg.msg_id,
                                   destination=msg.source,
                                   source=msg.destination))

    def _recv(self):
        """ Listen for messages and executes the callback function """
        while True:

            if self._adaptee.has_data():
                msg = self._adaptee.recv()

                if msg is None:
                    continue

                Log.log(MsgType.INFO, "Adapter - Reciving", msg)
                is_ack = msg.msg_type is Message.MsgType.ack

                if is_ack:
                    self._remove_ack_msg(msg)
                else:
                    # Send ACK
                    self._send_ack(msg)

                    # Execute command TIENE QUE SER ASYNC LO DE ABAJO
                    self._callback_func(msg)

            self._cleanup_unresponded_msgs()
