from commands.command_factory import CommandFactory
from command_controller.command_executor import CommandExecutor
from connection.net_adapter import NetAdapter
import multiprocessing
import unittest


class TestCommandExecutor(unittest.TestCase):

    def callback(self):
        pass

    def test_execute_cmds(self):

        dest = "dest"
        source = "source"

        cmsource = CommandExecutor(source)
        cmddest = CommandExecutor(dest)
        a1p, a2p = multiprocessing.Pipe(duplex=True)

        adapter1 = NetAdapter(destination=dest, callback_func=cmsource.enqueue_command, conn_obj=a2p)
        adapter2 = NetAdapter(destination=source, callback_func=cmddest.enqueue_command, conn_obj=a1p)

        cmsource.set_adapter(adapter1)
        cmddest.set_adapter(adapter2)

        param = [1, 2, 3]

        # Ack
        execute_at = -1
        cmd = CommandFactory.get_command(cmd_type=CommandFactory.CommandType.print, src=source, dest=dest, param=param,
                                         execute_at=execute_at)
        cmsource.enqueue_command(cmd)

        # Print
        execute_at = -1
        cmd = CommandFactory.get_command(CommandFactory.CommandType.print, source, dest, param, execute_at)
        cmddest.enqueue_command(cmd)

        # Error
        execute_at = -1
        cmd = CommandFactory.get_command(CommandFactory.CommandType.error, source, dest, param, execute_at)
        cmsource.enqueue_command(cmd)

        # Ack
        execute_at = -1
        cmd = CommandFactory.get_command(CommandFactory.CommandType.error, dest, source, param, execute_at)

        cmddest.enqueue_command(cmd)

        # Print
        execute_at = -1
        cmd = CommandFactory.get_command(CommandFactory.CommandType.print, dest, source, param, execute_at)
        cmsource.enqueue_command(cmd)

        # Error
        execute_at = -1
        cmd = CommandFactory.get_command(CommandFactory.CommandType.error, dest, source, param, execute_at)
        cmddest.enqueue_command(cmd)


if __name__ == '__main__':
    unittest.main()