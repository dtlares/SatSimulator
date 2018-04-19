from commands.command_factory import CommandFactory
from mission_units.ground_station import GroundStation
from mission_units.satellite import Satellite
import unittest


class TestMission(unittest.TestCase):

    def callback(self):
        pass

    def test_mission(self):

        ground = "ground"
        sat1 = "sat1"
        sat2 = "sat2"

        ground_station = GroundStation(ground)
        satellite1 = Satellite(sat1)
        satellite2 = Satellite(sat2)

        ground_station.create_connection(satellite1)
        ground_station.create_connection(satellite2)

        param = [1, 2, 3]

        # Ack
        execute_at = -1
        cmd = CommandFactory.get_command(cmd_type=CommandFactory.CommandType.print, src=ground, dest=sat1, param=param,
                                         execute_at=execute_at)
        ground_station.execute_command(cmd)

        '''
        # Print
        execute_at = -1
        cmd = CommandFactory.get_command(cmd_type=CommandFactory.CommandType.print, src=sat1, dest=ground, param=param,
                                         execute_at=execute_at)
        satellite1.execute_command(cmd)

        # Error
        execute_at = -1
        cmd = CommandFactory.get_command(cmd_type=CommandFactory.CommandType.error, src=ground, dest=sat2, param=param,
                                         execute_at=execute_at)
        ground_station.execute_command(cmd)

        # Ack
        execute_at = -1
        cmd = CommandFactory.get_command(cmd_type=CommandFactory.CommandType.print, src=sat2, dest=ground, param=param,
                                         execute_at=execute_at)
        satellite2.execute_command(cmd)

        # Print
        execute_at = -1
        cmd = CommandFactory.get_command(cmd_type=CommandFactory.CommandType.error, src=ground, dest=sat1, param=param,
                                         execute_at=execute_at)
        ground_station.execute_command(cmd)

        # Error
        execute_at = -1
        cmd = CommandFactory.get_command(cmd_type=CommandFactory.CommandType.error, src=sat1, dest=ground, param=param,
                                         execute_at=execute_at)
        satellite2.execute_command(cmd)
        '''

if __name__ == '__main__':
    unittest.main()