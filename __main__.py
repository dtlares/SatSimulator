""" Entry point of the simulation"""
from commands.command_factory import CommandFactory
from mission_units.satellite import Satellite
from mission_units.ground_station import GroundStation
from mission_units.task_planner import UnitTask, TasksPlanner


def main():
    """ Entry point of the mission simulation """
    # Create the task list
    task_list = [UnitTask(cmd_type=CommandFactory.CommandType.fotos, payoff=10, resources=[1, 5]),
                 UnitTask(cmd_type=CommandFactory.CommandType.mantenimiento, payoff=1, resources=[1, 2]),
                 UnitTask(cmd_type=CommandFactory.CommandType.pruebas, payoff=1, resources=[5, 6]),
                 UnitTask(cmd_type=CommandFactory.CommandType.fsck, payoff=0.1, resources=[1, 6])]

    # Perform a optimized task selection
    task_list = TasksPlanner.get_plan(2, task_list)

    ground = "ground"
    sat1 = "sat1"
    sat2 = "sat2"

    destinations = [sat1, sat2]

    # Create a list of commands based on the tasks list
    cmd_list = TasksPlanner.build_commands(task_list, ground, destinations)

    # Start the mission units
    ground_station = GroundStation(ground)
    satellite1 = Satellite(sat1)
    satellite2 = Satellite(sat2)

    ground_station.create_connection(satellite1)
    ground_station.create_connection(satellite2)

    destinations_count = len(destinations)

    # Send the commands
    for index in range(0, destinations_count):
        for cmd in cmd_list[index]:
            ground_station.execute_command(cmd)


if __name__ == '__main__':
    main()
