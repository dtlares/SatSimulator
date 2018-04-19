""" This module is for the FSCK command """
import random
from .command import Command


class CmdManteniento(Command):
    """  Performs maintenance tasks """

    @Command.set_timestamp
    def execute_command(self):
        """  Performs maintenance tasks """
        self.status = Command.Status.in_progress
        print("Performs maintenance! " + self.__str__())
        rnd_num = random.uniform(1, 10)
        self.status = Command.Status.failed if rnd_num <= Command.error_threshold else self.status
        return self.status
