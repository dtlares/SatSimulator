""" This module provides a factory to create commands"""
import datetime
from enum import Enum
from .cmd_error import CmdError
from .cmd_pruebas import CmdPruebas
from .cmd_fotos import CmdFotos
from .cmd_print import CmdPrint
from .cmd_fsck import CmdFSCK
from .cmd_mantenimiento import CmdManteniento


class CommandFactory:
    """ Command Factory: Creates different command objects"""

    class CommandType(Enum):
        """ Enum with all supported Command types"""
        error = CmdError
        print = CmdPrint
        fotos = CmdFotos
        pruebas = CmdPruebas
        fsck = CmdFSCK
        mantenimiento = CmdManteniento

    @staticmethod
    def get_command(cmd_type: CommandType, src: str, dest: str, param: list, execute_at: int = -1):
        """ Creates a command based in an input type
            cmd_type: The type of the commmand (Fotos, Pruebas, Mantenimiento)
            src: the source of the command
            dest: the location where the command must be executed
            param: a list of parameters
            execute_at: the moment that the command must be executed
        """
        cmd_id = datetime.datetime.now()
        cmd = cmd_type.value(cmd_id=cmd_id, source=src, dest=dest, cmd_type=cmd_type, param=param,
                             execute_at=execute_at)
        return cmd
