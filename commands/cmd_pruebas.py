""" This module is for the pruebas command """
import random
from .command import Command


class CmdPruebas(Command):
    """  Performs testing tasks """

    @Command.set_timestamp
    def execute_command(self):
        """  Performs testing tasks """
        self.set_timestamp()
        self.status = Command.Status.in_progress
        print("Testing! " + self.__str__())
        rnd_num = random.uniform(1, 10)
        self.status = Command.Status.failed if rnd_num <= Command.error_threshold else self.status
        return self.status
