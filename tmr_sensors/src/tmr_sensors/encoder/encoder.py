import numpy as np
from tmr_sensors.sensors import Sensors

class Encoder(Sensors):
    """
    Encoder class, this class will simulate the encoder of a wheel
    When the wheel rotates, the value of the wheel angles are continously monitored
    depending on the resolution. The system also has option to add a noise model
    """

    def __init__(self, robot_interface, config):
        """
        The class that logs in econder readings of the robot
        Takes in robot interface as the key argument This class is of type tmr_robot.robot
        """

        Sensors.__init__(self, robot_interface, config)

        self.reset()

        self.enable()

    def update(self):
        """
        The function that updates the values of the sensors
        """

        if self._is_active:

            self._curr_value = self._robot.wheel_omgs()/self._res + self.noise()

    def reset(self):
        """
        to reset the value of the sensors
        """

        self._curr_value = np.zeros(self._robot._num_wheels)

    def noise(self):
        """
        add noise to the sensor readings
        depending on the sensor noise, you can change this funciton
        """

        if self._noise_type == 'random':

            return self._noise_gain*np.random.randn(self._robot._num_wheels)