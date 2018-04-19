""" The command executor module includes classes that process commands.
    If the command destination matches with the unit name, it is executed locally,
    otherwise it is sent to a different adapter """

from commands.command import Command
from command_controller.command_encoding import CommandEncoding
from connection.msg_pkg import Message
from connection.net_adapter import NetAdapter
from utils.log import Log, MsgType


class CommandExecutor:
    """ Processes a command queue and executes it"""

    def __init__(self, unit_name: str, validation_pool=None):
        """ The class constructor
            unit_name: the name of the unit that uses this Command executor
            validation_pool: the validation component that waits for an executed command"""
        self._unit_name = unit_name
        self._sender = None
        self._command_queue = []
        self._thread_paused = True
        self._thread_stop = False
        self._validator = validation_pool

    def get_adapter(self):
        """ Returns the adapter"""
        return self._sender

    def set_adapter(self, sender: NetAdapter):
        """ Sets the adapter """
        self._sender = sender

    def enqueue_command(self, data):
        """ Adds a command to be processed """
        cmd = data

        if isinstance(data, Message):
            if data.data is None or isinstance(data.data, str):
                return
            cmd = CommandEncoding.command_decoder(data.data)
            if data.msg_type is Message.MsgType.executed:
                self._validator.validate_response(cmd)
                return
            elif data.msg_type is Message.MsgType.ack:
                return

        if cmd.dest != cmd.source and cmd.execute_at <= 0:
            self._command_queue.append(cmd)
            self._execute_commands()

    def _execute_commands(self):
        """ If the command destination matches with the unit, it is executed locally.
            Otherwise it is sent to another module using the adapter (sender)"""
        remove_cmd = []
        for cmd in self._command_queue:

            # Handle Command: this command must be processed by this unit
            if cmd.dest == self._unit_name:

                Log.log(MsgType.INFO, "CMD Executor - Executing CMD", str(cmd.cmd_id))

                cmd.execute_command()
                cmd.status = Command.Status.executed

                status = Message.MsgType.executed if cmd.status is not Command.Status.failed else Command.Status.failed
                data = CommandEncoding.command_encoder(cmd)
                msg = Message(msg_type=status, msg_id=cmd.cmd_id, destination=cmd.source,
                              source=cmd.dest, data=data)

                self._sender(msg)

            # This command must be sent to other unit
            else:
                Log.log(MsgType.INFO, "CMD Executor - Sending command to %s" % cmd.dest, str(cmd.cmd_id))
                # Command encode
                cmd.status = Command.Status.in_progress
                data = CommandEncoding.command_encoder(cmd)
                msg = Message(msg_type=Message.MsgType.command, msg_id=cmd.cmd_id, destination=cmd.dest,
                              source=cmd.source, data=data)
                Log.log(MsgType.INFO, "CMD Executor - Sending", str(cmd.cmd_id))
                self._sender(msg)

                if self._validator is not None:
                    self._validator.add_command(cmd)

            # Command cleanup
            remove_cmd.append(cmd)

        for cmd in remove_cmd:
            #self._command_queue.remove(cmd)
            del cmd
