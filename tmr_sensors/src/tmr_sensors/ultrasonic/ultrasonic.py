#!/usr/bin/env python3
"""Provides Ultrasonic sensor class. Fully runtime configurable
sensors depending on the config file

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

class Ultrasonic(Sensors):
    """
    The laser class used to measure the distance to nearest obstacle.
    The value depends on the total range of the sytem and resolution of the device
    The system also has an option to add new noise model into the system.
    """

    def __init__(self, robot_interface, config):

        Sensors.__init__(self, robot_interface, config)

        self.reset()

        self.enable()

        self._robot = robot_interface

        if config['obstacle_config'] is not None:

            self._obs_config = config['obstacle_config']

            if 'obstacles_start' in self._obs_config and 'obstacles_end' in self._obs_config:

                self._obstacle_lines_starts = self._obs_config['obstacles_start']

                self._obstacle_lines_ends = self._obs_config['obstacles_end']

            assert len(self._obstacle_lines_starts) == len(self._obstacle_lines_ends)


    def update(self):
        """
        Update the value of the sensors d
        for reading. It takes in input from the world state and depending on 
        if there is an obstacle, the system updates the input
        """

        rs = self._robot.robot_true_state()

        def detect_obstacle(obs_s, obs_e):
            """
            a simple algo to detect collission between
            circle and line segment between obs_s, obs_e
            rs is the location of the robot and radius of the robot
            """
            a = obs_s[1]-obs_e[1]

            b = obs_e[0]-obs_s[0]

            c = -b*obs_s[1] -a*obs_s[0]

            dist = np.abs(a*rs[0] + b*rs[1] + c)/np.linalg.norm(obs_s-obs_e) + self.noise()

            if dist <= self._range:

                return dist

            else:

                return np.nan

        if self._is_active:
        
            dists = []

            for s, e in zip(self._obstacle_lines_starts, self._obstacle_lines_ends):

                dists.append(detect_obstacle(s, e))

            self._curr_value = np.array(dists)
        

    def reset(self):
        #first row will will be collision point in x 
        #second row will be collision point in y
        self._curr_value = np.ones(self._robot._num_lasers)*self._range


    def noise(self):
        """
        Add noise to the sensor values
        """
        if self._noise_type == 'random':

            return self._noise_gain*np.random.randn(self._robot._num_lasers)
            
        else:

            raise NotImplementedError("Asking for a noise model that is unknown")
