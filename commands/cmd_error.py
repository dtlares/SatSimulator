""" This module is for the Error command """
from .command import Command


class CmdError(Command):
    """ Represents a command failed"""

    @Command.set_timestamp
    def execute_command(self):
        """Executes error command"""
        self.set_timestamp()
        self.status = Command.Status.executed
        self.payload = "Error"
        return self.status
