""" This module is for the print command """
import random
from .command import Command


class CmdPrint(Command):
    """ Prints a string with command info"""

    @Command.set_timestamp
    def execute_command(self):
        """ Prints a string with command info"""
        self.set_timestamp()
        self.status = Command.Status.in_progress
        print(self.__str__)
        rnd_num = random.uniform(1, 10)
        self.status = Command.Status.failed if rnd_num <= Command.error_threshold else self.status
        return self.status
