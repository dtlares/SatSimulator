""" The Ground Station component """
import multiprocessing
from connection.net_demultiplexer import DeMultiplexer
from connection.net_adapter import NetAdapter
from mission_units.mission_unit import MissionUnit


class GroundStation(MissionUnit):
    """ The Ground Station class """

    def __init__(self, name: str):
        """ Constructor
            name: the name of the ground station
            """
        super().__init__(name)
        self._demultiplexer = DeMultiplexer()

    def set_adapter(self, adapter):
        """ This should no be used in this class"""
        pass

    def create_connection(self, unit):
        """ Creates a connection with the unit. Creates and attaches the adapters"""
        satellite_name = unit.get_name()

        if not self._demultiplexer.connection_exists(satellite_name):

            a1p, a2p = multiprocessing.Pipe(duplex=True)

            ground_adapter = NetAdapter(destination=satellite_name, callback_func=self.get_command_callback(),
                                        conn_obj=a2p)

            sat_adapter = NetAdapter(destination=self._name, callback_func=unit.get_command_callback(), conn_obj=a1p)
            unit.set_adapter(sat_adapter)

            self._demultiplexer.add_connection(satellite_name, ground_adapter)
            self._command_executor.set_adapter(self._demultiplexer)
