#!/usr/bin/env python3
"""Provides base sensor class. Fuly extendable to any other sensors
Any new sensor module created should be a child of this class

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

import abc

class Sensors(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, robot_interface, config):

        self.init_sensor(config)

        self._curr_value = None

        self._robot = robot_interface
        
        self.disable()


    def init_sensor(self, config):

        self._config = config

        self._name = config['name']

        self._res = config['params']['res']

        self._noise_gain = config['params']['noise_gain']

        self._noise_type = config['noise_type']

        self._range = config['params']['range']

        self._val_dim = config['val_dim']

        self._plotable_vals = config['plotable_vals']


    @abc.abstractmethod
    def update(self):

        raise NotImplementedError("Must be implemented in the subclass")

    @abc.abstractmethod
    def reset(self):

        raise NotImplementedError("Must be implemented in the subclass")


    @abc.abstractmethod
    def noise(self):

        raise NotImplementedError("Must be implemented in the subclass")


    def config(self):
        return self._config

    def name(self):
        return self._name

    def reading(self):

        return self._curr_value

    def enable(self):

        self._is_active = True

    def disable(self):

        self._is_active = False
