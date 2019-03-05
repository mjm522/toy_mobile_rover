#!/usr/bin/env python3
"""Provides rover class. This function integrates the robot
with the sensors

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

import datetime

class Rover():

    def __init__(self, config):
        """
        The class which combines the robot with the sensors.
        """

        self._robot = config['robot']

        self._robot.init_start(x0=2.0, y0=3.5, alpha0=0.)

        self._sensors = config['sensors'] 

    def command_robot(self, u):
        """
        The function that sends commnads to the robto
        inputs : u = control commands of the left and right wheel
        """

        true_state = self._robot.step(u)

        for sensor in self._sensors:

            sensor.update()

        return true_state

    def stop(self):
        """
        The utility function to insteneously stop the robot
        """
        self._robot.stop()


    def reset(self, x):
        """
        Reset the rover
        """

        self._robot.init_start(x0=x[0], y0=x[1], alpha0=x[2])


    def update_robot_config(self, robot_config):
        """
        Change the robot configuration with respect
        to the user input from the gui
        """

        self._robot.init_robot(robot_config)


    def update_sensor_config(self, sensor_config, idx):
        """
        Change the sensor configuration with respect
        to the user input from the gui
        """

        self._sensors[idx].init_sensor(sensor_config)


    def sensed_state(self):
        """
        This the key dictionary of values
        It contains the sensor readings of all the sytems in place
        """
        robot_state = {'time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        for sensor in self._sensors:
            
            robot_state[sensor.name()]=sensor.reading()

        return robot_state

    def true_state(self):
        """
        For debugging purposes
        and can be used for reseting the robot
        """
        return self._robot.robot_true_state()

    def compute_rot_mat(self):
        """
        utility funciton to compute the current rotation
        matrix of the robot
        """

        return self._robot.compute_rot_mat()
