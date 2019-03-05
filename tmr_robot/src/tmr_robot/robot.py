#!/usr/bin/env python3
"""The following file depicts robot interface of the real robot
The dynamics of the robot is not considered
The robot is assumed to get wheel angular velocities as input
The system takes in the input and create the corresponding motion from the system.

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
from tmr_sensors.utils.utils import rk4_average


class Robot():

    def __init__(self, config):
        """
        Class constructor for the robot class.
        The input is a config file is a python dict consisting of the following parameters
        dt = runge-kutta integration time constant
        step_size = step size of the world
        wheel_r = radius of the wheel
        robot_r = the robot is assumed to be a round robot with a radius
        """

        self.init_robot(config)

        self._num_wheels=2

        self._num_lasers=1

        self._wheel_omgs = [0]*self._num_wheels


    def init_robot(self, config):

        self._config = config

        self._dt = config['params']['dt']

        self._t  = 0.

        self._step_size = config['params']['step_size']

        self._wheel_r = config['params']['wheel_r']

        self._robot_d = 2*config['params']['robot_r']

        self._wheel_omg_limit = config['params']['wheel_omg_limit']

        assert self._wheel_r > 0.

        assert self._robot_d > 0.

        assert self._step_size >= self._dt

    def config(self):

        return self._config


    def init_start(self, x0, y0, alpha0, t0=0):
        """
        Initialise the starting pose of the robot
        x0 = initial x position
        y0 = initial y position
        alpha0 = initial angular position
        t0 = initial time
        """
        self._x = np.array([x0, y0, alpha0, 0., 0., 0.])

        self._t = t0


    def stop(self):

        self._x[3:] = np.zeros(3)


    def wheel_omgs(self):

        return np.asarray(self._wheel_omgs)


    def robot_true_state(self):

        return self._x.copy()

    def compute_rot_mat(self):

        rover_rot = np.array([ [np.cos(self._x[2]), -np.sin(self._x[2])], 
                               [np.sin(self._x[2]),  np.cos(self._x[2])] ])
        return rover_rot
 
    def kinematics(self, x, u):
        """
        To compute the kinematics of the robot
        u[0] = omega of right wheel
        u[1] = omeaga of left wheel
        """
        #this assumption is right only since we don't have a controller on board
        #and assumes the robot is able to instentaneoulsy set the the wheel velocity
        #to the commanded effort
        self._wheel_omgs = u

        #right and left wheel linear velocity
        vel_r = u[0]*self._wheel_r

        vel_l = u[1]*self._wheel_r

        #average forward velocity of the robot
        vel_avg = 0.5*(vel_r + vel_l)
        
        #derivative of state the robot
        x3_dt = (u[0] - u[1])*(self._wheel_r/self._robot_d)

        x2_dt = vel_avg*np.sin(x[2]+x3_dt)*self._robot_d

        x1_dt = vel_avg*np.cos(x[2]+x3_dt)*self._robot_d

        return [ x[3], x[4], x[5], x1_dt, x2_dt, x3_dt ]

    def rk4_integrate(self, u, dt):
        """
        Perform runge-kutta integration of the robot next position
        the integration time step is specified in the config file
        """

        dx = self.kinematics(self._x, u)
        k2 = [ dx_i*dt for dx_i in dx ]

        xv = [x_i + delx0_i/2.0 for x_i, delx0_i in zip(self._x, k2)]
        k3 = [ dx_i*dt for dx_i in self.kinematics(xv, u)]

        xv = [x_i + delx1_i/2.0 for x_i,delx1_i in zip(self._x, k3)]
        k4 = [ dx_i*dt for dx_i in self.kinematics(xv, u) ]

        xv = [x_i + delx1_2 for x_i,delx1_2 in zip(self._x, k4)]
        k1 = [self._dt*i for i in self.kinematics(xv, u)]

        self._t += dt
        self._x = np.asarray(list(map(rk4_average, zip(self._x, k1, k2, k3, k4))))


    def step(self, u):
        """
        The robot steps through the world for 
        control command u for the given step size
        """

        u[ u > self._wheel_omg_limit ] = self._wheel_omg_limit
        u[ u < -self._wheel_omg_limit ] = -self._wheel_omg_limit

        while self._t <= self._step_size:

            self.rk4_integrate(u, self._dt)

        self._t = 0

        self.compute_rot_mat()

        return self.robot_true_state()

