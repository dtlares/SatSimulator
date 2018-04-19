""" The basic unit of the Mission. Can be extended to different scenarios"""
from command_controller.command_executor import CommandExecutor
from command_controller.command_validator import CommandValidator


class MissionUnit:
    """ Mission Unit """
    def __init__(self, name: str):
        """ Constructor
            name: the name of the ground station
            """
        super().__init__()
        self._name = name
        self._command_validator = CommandValidator()
        self._command_executor = CommandExecutor(self._name, self._command_validator)

    def get_name(self):
        """ Returns the name of the unit"""
        return self._name

    def get_command_callback(self):
        """ Returns the command processor callback """
        return self._command_executor.enqueue_command

    def create_connection(self, unit):
        """ Creates a connection with the unit """
        pass

    def set_adapter(self, adapter) -> bool:
        """ Set the connection adapter """
        if self._command_executor.get_adapter() is None:
            self._command_executor.set_adapter(adapter)
            return True

        return False

    def execute_command(self, *args):
        """ Executes a command """
        for cmd in args:
            self._command_executor.enqueue_command(cmd)
