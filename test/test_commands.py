from commands.command_factory import CommandFactory
import datetime
import unittest


class TestCommands(unittest.TestCase):

    def test_ack(self):
        source = "source"
        dest = "dest"
        param = [1, 2, 3]
        execute_at = datetime.datetime.now()
        cmd = CommandFactory.get_command(CommandFactory.CommandType.print, source, dest, param, execute_at)
        status = cmd.execute_command()
        self.assertEqual(cmd.source, source)
        self.assertEqual(cmd.dest, dest)
        self.assertEqual(cmd.param, param)
        self.assertEqual(cmd.execute_at, execute_at)

    def test_error(self):
        source = "source"
        dest = "dest"
        param = [1, 2, 3]
        execute_at = datetime.datetime.now()
        cmd = CommandFactory.get_command(CommandFactory.CommandType.error, source, dest, param, execute_at)
        status = cmd.execute_command()
        self.assertEqual(cmd.source, source)
        self.assertEqual(cmd.dest, dest)
        self.assertEqual(cmd.param, param)
        self.assertEqual(cmd.execute_at, execute_at)

    def test_print(self):
        source = "source"
        dest = "dest"
        param = [1, 2, 3]
        execute_at = datetime.datetime.now()
        cmd = CommandFactory.get_command(CommandFactory.CommandType.print, source, dest, param, execute_at)
        status = cmd.execute_command()
        self.assertEqual(cmd.source, source)
        self.assertEqual(cmd.dest, dest)
        self.assertEqual(cmd.param, param)
        self.assertEqual(cmd.execute_at, execute_at)


if __name__ == '__main__':
    unittest.main()
