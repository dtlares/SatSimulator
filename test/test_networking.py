from connection.net_adapter import NetAdapter
from connection.msg_pkg import Message
import multiprocessing
import time
import unittest


class TestNetworking(unittest.TestCase):

    @staticmethod
    def callback(msg: Message):
        print("Message received %f - Sent from %s  to %s" % (msg.msg_id, msg.data, msg.destination))

    def test_adapters(self):

        dest = "dest"
        src = "source"

        a1p, a2p = multiprocessing.Pipe(duplex=True)

        adapter1 = NetAdapter(destination=dest, callback_func=self.callback, conn_obj=a2p)
        adapter2 = NetAdapter(destination=src, callback_func=self.callback, conn_obj=a1p)

        msg1 = Message(msg_id=time.time(), msg_type=Message.MsgType.command, destination=dest, source=src, data=src)
        adapter1.send(msg1)

        msg2 = Message(msg_id=time.time(), msg_type=Message.MsgType.command, destination=src, source=dest, data=dest)
        adapter2.send(msg2)

        msg1 = Message(msg_id=time.time(), msg_type=Message.MsgType.command, destination=dest, source=src, data=src)
        adapter1.send(msg1)

        msg2 = Message(msg_id=time.time(), msg_type=Message.MsgType.command, destination=src, source=dest, data=dest)
        adapter2.send(msg2)

        msg1 = Message(msg_id=time.time(), msg_type=Message.MsgType.command, destination=dest, source=src, data=src)
        adapter1.send(msg1)

        msg2 = Message(msg_id=time.time(), msg_type=Message.MsgType.command, destination=src, source=dest, data=dest)
        adapter2.send(msg2)

        msg1 = Message(msg_id=time.time(), msg_type=Message.MsgType.command, destination=dest, source=src, data=src)
        adapter1.send(msg1)

        msg2 = Message(msg_id=time.time(), msg_type=Message.MsgType.command, destination=src, source=dest, data=dest)
        adapter2.send(msg2)

        msg1 = Message(msg_id=time.time(), msg_type=Message.MsgType.command, destination=dest, source=src, data=src)
        adapter1.send(msg1)

        msg2 = Message(msg_id=time.time(), msg_type=Message.MsgType.command, destination=src, source=dest, data=dest)
        adapter2.send(msg2)

        msg1 = Message(msg_id=time.time(), msg_type=Message.MsgType.command, destination=dest, source=src, data=src)
        adapter1.send(msg1)

        msg2 = Message(msg_id=time.time(), msg_type=Message.MsgType.command, destination=src, source=dest, data=dest)
        adapter2.send(msg2)

        msg1 = Message(msg_id=time.time(), msg_type=Message.MsgType.command, destination=dest, source=src, data=src)
        adapter1.send(msg1)

        msg2 = Message(msg_id=time.time(), msg_type=Message.MsgType.command, destination=src, source=dest, data=dest)
        adapter2.send(msg2)


if __name__ == '__main__':
    unittest.main()
