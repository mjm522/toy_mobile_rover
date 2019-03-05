#!/usr/bin/env python3
"""Contains utilty function for the world file
so as to move around

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

def convert_screen_to_world(screen_x, screen_y, ppm, screen_ht):
    """
    utility function to converte screen pixel coordinates to the world coordinates
    """
    return np.array([float(screen_x)/ppm , float(screen_ht-screen_y)/ppm])


def make_obstacle_world(map_config, ppm, screen_ht):

    map_obstacles_start = []
    map_obstacles_end = []

    if map_config['wall_corners'] is not None:
        for l, s in zip(map_config['wall_corners'], map_config['wall_size']):

            map_obstacles_start.append(convert_screen_to_world(l[0], l[1], ppm, screen_ht ))
            map_obstacles_end.append(convert_screen_to_world(s[0], s[1], ppm, screen_ht ))


    if map_config['obstacles_locations'] is not None:
        for l, s in zip(map_config['obstacles_locations'], map_config['obstacles_size']):

            map_obstacles_start.append(convert_screen_to_world(l[0], l[1], ppm, screen_ht) )
            map_obstacles_end.append(convert_screen_to_world(s[0], s[1], ppm, screen_ht ))

    return {'obstacles_start':map_obstacles_start, 'obstacles_end':map_obstacles_end}