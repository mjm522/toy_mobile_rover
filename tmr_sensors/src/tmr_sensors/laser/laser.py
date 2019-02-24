import numpy as np
from tmr_sensors.sensors import Sensors

class Laser():
    """
    The laser class used to measure the distance to nearest obstacle.
    The value depends on the total range of the sytem and resolution of the device
    The system also has an option to add new noise model into the system.
    """

    def __init__(self, robot_interface, config):

        Sensors.__init__(self, robot_interface, config)


    def update(self):
        pass


    def reset(self):
        pass