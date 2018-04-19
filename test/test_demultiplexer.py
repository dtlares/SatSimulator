from commands.command_factory import CommandFactory
from command_controller.command_executor import CommandExecutor
from connection.net_adapter import NetAdapter
from connection.net_demultiplexer import DeMultiplexer
import multiprocessing
import unittest


class TestDemultiplexer(unittest.TestCase):

    def callback(self):
        pass

    def test_demultiplexer(self):

        sat1 = "sat1"
        sat2 = "sat2"
        ground = "ground"

        cm_ground = CommandExecutor(ground)
        cm_sat1 = CommandExecutor(sat1)
        cm_sat2 = CommandExecutor(sat2)

        grn_demult = DeMultiplexer()

        sat1_grn, grn_sat1 = multiprocessing.Pipe(duplex=True)
        sat2_grn, grn_sat2 = multiprocessing.Pipe(duplex=True)

        ground_sat1_adapter = NetAdapter(destination=sat1, callback_func=cm_ground.enqueue_command, conn_obj=grn_sat1)
        sat1_adapter = NetAdapter(destination=ground, callback_func=cm_sat1.enqueue_command, conn_obj=sat1_grn)

        ground_sat2_adapter = NetAdapter(destination=sat2, callback_func=cm_ground.enqueue_command, conn_obj=grn_sat2)
        sat2_adapter = NetAdapter(destination=ground, callback_func=cm_sat2.enqueue_command, conn_obj=sat2_grn)

        grn_demult.add_connection(sat1, ground_sat1_adapter)
        grn_demult.add_connection(sat2, ground_sat2_adapter)

        cm_ground.set_adapter(grn_demult)
        cm_sat1.set_adapter(sat1_adapter)
        cm_sat2.set_adapter(sat2_adapter)

        param = [1, 2, 3]

        # Ack
        execute_at = -1
        cmd = CommandFactory.get_command(cmd_type=CommandFactory.CommandType.print, src=ground, dest=sat1, param=param,
                                         execute_at=execute_at)
        cm_ground.enqueue_command(cmd)

        # Print
        execute_at = -1
        cmd = CommandFactory.get_command(cmd_type=CommandFactory.CommandType.print, src=sat1, dest=ground, param=param,
                                         execute_at=execute_at)
        cm_sat1.enqueue_command(cmd)

        # Error
        execute_at = -1
        cmd = CommandFactory.get_command(cmd_type=CommandFactory.CommandType.error, src=ground, dest=sat2, param=param,
                                         execute_at=execute_at)
        cm_ground.enqueue_command(cmd)

        # Ack
        execute_at = -1
        cmd = CommandFactory.get_command(cmd_type=CommandFactory.CommandType.print, src=sat2, dest=ground, param=param,
                                         execute_at=execute_at)
        cm_sat2.enqueue_command(cmd)

        # Print
        execute_at = -1
        cmd = CommandFactory.get_command(cmd_type=CommandFactory.CommandType.error, src=ground, dest=sat1, param=param,
                                         execute_at=execute_at)
        cm_ground.enqueue_command(cmd)

        # Error
        execute_at = -1
        cmd = CommandFactory.get_command(cmd_type=CommandFactory.CommandType.error, src=sat1, dest=ground, param=param,
                                         execute_at=execute_at)
        cm_sat1.enqueue_command(cmd)


if __name__ == '__main__':
    unittest.main()