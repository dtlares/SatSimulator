""" Command Validator provides tools to validate response messages """
from commands.command import Command


class CommandValidator:
    """ Functions to validate sent command responses"""
    def __init__(self):
        self._command_list = []

    def add_command(self, cmd: Command):
        """ Adds a command to be validated """
        self._command_list.append(cmd)

    def validate_response(self, cmd):
        """Validates command response"""

        cmd_to_remove = []
        for stored_command in self._command_list:
            if cmd.cmd_id == stored_command.cmd_id:
                if cmd.status == Command.Status.executed:
                    print("Command executed successfully - %s" % cmd)
                elif cmd.status == Command.Status.failed:
                    print("Command Failed!! - %s" % cmd)
                else:
                    print("Unhandled command status - %s" % cmd)

                    cmd_to_remove.append(cmd)

        for stored_command in cmd_to_remove:
            self._command_list.remove(stored_command)
