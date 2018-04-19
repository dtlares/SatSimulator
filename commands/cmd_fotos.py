""" This module is for the Fotos command """
import random
from .command import Command


class CmdFotos(Command):
    """  Takes a photo """

    @Command.set_timestamp
    def execute_command(self):
        """  Takes a photo """
        self.set_timestamp()
        self.status = Command.Status.in_progress
        print("Taking a photo! " + self.__str__())
        rnd_num = random.uniform(1, 10)
        self.status = Command.Status.failed if rnd_num <= Command.error_threshold else self.status
        return self.status
