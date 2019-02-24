import numpy as np
from tmr_sensors.sensors import Sensors

class Encoder():
    """
    Encoder class, this class will simulate the encoder of a wheel
    When the wheel rotates, the value of the wheel angles are continously monitored
    depending on the resolution. The system also has option to add a noise model
    """

    def __init__(self, robot_interface, config):

        Sensors.__init__(self, robot_interface, config)

    def update(self):
        pass


    def reset(self):
        pass