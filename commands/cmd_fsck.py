""" This module is for the FSCK command """
import random
from .command import Command


class CmdFSCK(Command):
    """  Performs FSCK """

    @Command.set_timestamp
    def execute_command(self):
        """  Performs FSCK """
        self.set_timestamp()
        self.status = Command.Status.in_progress
        print("FSCK! " + self.__str__())
        rnd_num = random.uniform(1, 10)
        self.status = Command.Status.failed if rnd_num <= Command.error_threshold else self.status
        return self.status
