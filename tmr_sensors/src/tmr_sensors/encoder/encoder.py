#!/usr/bin/env python3
"""Provides an encoder class for the robot
The class contains an econder with fully run time configurable 
files from the config file.

Copyright (C) 2019 Michael J Mathew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

__author__     = "Michael J Mathew"
__copyright__  = "Copyright 2019, The Ascent Project"
__license__    = "GNU"
__version__    = "0.0.0"
__maintainer__ = "Michael J Mathew"
__email__      = "mjm522@student.bham.ac.uk"
__status__     = "Development"

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