#!/usr/bin/env python3
"""Provides world class. This is mainly to integrate the rover to the world
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


import os
import copy
import pygame
import logging
import numpy as np
from math import fabs
from tmr_world.sprites import Wall, Agent

logging.getLogger().setLevel(logging.INFO)


class World():

    def __init__(self, rover_interface, config):
        """
        Class constructor. 
        Params: rover_interface - type tmr_rover.rover
                config - type tmr_world.config
        """

        self._fps               = config['FPS']

        self._ppm               = config['PPM']

        self._bg_color          = config['bg_color']

        self._laser_color       = config['laser_color']

        self._laser_alpha       = config['laser_alpha']

        self._robot_color       = config['robot_color']

        self._display_width     = config['screen_width']

        self._display_height    = config['screen_height']

        self._motor_increment   = config['motor_increment']

        self._laser_sensor_idx  = config['laser_sensor_idx']

        self._rover             = rover_interface

        self._done              = False

        self._show_log          = False

        self._move_own          = True

        self._motor_1_cmd       = 0.

        self._motor_2_cmd       = 0.

        pygame.init()

        self._clock             = pygame.time.Clock()

        self._font              = pygame.font.SysFont(None, 25)
        
        self._display_screen    = pygame.display.set_mode((self._display_width, self._display_height))

        self._curr_robot_y      = None

        self._curr_robot_x      = None

        pygame.display.set_caption('Toy Mobile Rover')

        self.init_map(config['map_config'])

        self.init_robot()

        self.init_keyboard_ctrl()


    def init_keyboard_ctrl(self):
        """
        Instantiate the keyboard control
        Currently it is set to intermittently
        control the robot from the keyboard
        """


        self._pressed_up    =  False

        self._pressed_down  =  False

        self._pressed_left  =  False

        self._pressed_right =  False


    def init_map(self, map_config):
        """
        The function that initiates the map
        The map is configurable by chaning parameters
        of the map_config available at tmr_world.config
        The coordinates in the config file is given as pixel coordinates
        """

        if map_config is None:

            return
        
        # self._wall_list = pygame.sprite.Group()

        self._all_sprites_list = pygame.sprite.Group()

        self._obstacles = []

        if map_config['wall_corners'] is not None:

            for l, s in zip(map_config['wall_corners'], map_config['wall_size']):

                block = Wall(map_config['wall_color'], s[0], s[1])

                block.rect.x = l[0]

                block.rect.y = l[1]

                # self._wall_list.add(block)

                self._all_sprites_list.add(block)

                self._obstacles.append([l[0],l[1],s[0],s[1]])

        if map_config['obstacles_locations'] is not None:

            for l, s in zip(map_config['obstacles_locations'], map_config['obstacles_size']):

                block = Wall(map_config['obstacle_color'], s[0], s[1])

                block.rect.x = l[0]

                block.rect.y = l[1]

                # self._wall_list.add(block)

                self._all_sprites_list.add(block)

                self._obstacles.append([l[0],l[1],s[0],s[1]])


    def update_sensor_config(self, new_sensor_config, idx):
        """
        The function that updates the sensor configuration
        based on a snesor index as dictated by the user
        via the gui
        """

        self._rover.update_sensor_config(new_sensor_config, idx)

        self.init_robot()

    def update_robot_config(self, new_robot_config):
        """
        The key function that will called back from the 
        gui to update the parameters of the dictionary
        Params: new_robot_config = type dictionary of values
        """

        self._rover.update_robot_config(new_robot_config)

        self.init_robot()

    def has_collided_with(self,  mob):
        """
        Collision checker core.
        The idea is to check collision with multiple
        lines in the block and stop the robot when a
        collision is detected. This needs further polishing
        Params: mob = the block object
        """

        if self._curr_robot_x and self._curr_robot_y:

            robot_radius  = int(0.5*self._rover._robot._robot_d*self._ppm)

            obst_rect     = np.array([mob[0],mob[1], mob[0]+mob[2], mob[1]+mob[3]])

            robot_center  = np.array([self._curr_robot_x,self._curr_robot_y]).squeeze()

            # print (obst_rect[:2], robot_center,(np.linalg.norm(robot_center - obst_rect[:2])))

            if ((np.linalg.norm(robot_center - obst_rect[:2])) <= robot_radius) or \
                ((np.linalg.norm(robot_center - obst_rect[2:])) <= robot_radius) or \
                ((np.linalg.norm(robot_center - obst_rect[:2] - np.array([mob[2],0]))) <= robot_radius) or \
                ((np.linalg.norm(robot_center - obst_rect[:2] - np.array([mob[2],mob[3]]))) <= robot_radius) or \
                ((np.linalg.norm(robot_center - obst_rect[:2] - 0.5*np.array([mob[2],mob[3]]))) <= 1.2*robot_radius):

                return True

        return False


    def collision_check(self):
        """
        A rudimentary collision checking algorithm
        to detect collision of lines with circles
        """

        for block in self._obstacles:
            
            if self.has_collided_with( block ):

                return True

        return False  


    def init_robot(self):
        """
        They key part that draws the robot
        """

        robot_radius = int(0.5*self._rover._robot._robot_d*self._ppm)

        laser_radius = int(self._rover._sensors[self._laser_sensor_idx]._range*self._ppm)

        self._robot_surface = pygame.Surface((robot_radius*2,robot_radius*2))
        
        self._robot_surface.set_colorkey(self._bg_color)
        
        pygame.draw.circle(self._robot_surface, self._robot_color, (robot_radius, robot_radius), robot_radius)
        
        pygame.draw.polygon(self._robot_surface, (0,0,255), [[robot_radius,robot_radius-10],\
                                                             [robot_radius,robot_radius+10],\
                                                             [2*robot_radius,robot_radius+10],\
                                                             [2*robot_radius,robot_radius-10]], 2)

        self._global_robot = self._robot_surface

        self._robot_sensor_surface = pygame.Surface((laser_radius*2,laser_radius*2))
        
        self._robot_sensor_surface.set_colorkey(self._bg_color)
        
        self._robot_sensor_surface.set_alpha(self._laser_alpha)
        
        pygame.draw.circle(self._robot_sensor_surface, self._laser_color, (laser_radius, laser_radius), laser_radius)

        self._global_robot_sensor_surface = self._robot_sensor_surface
            
    def key_board_menu_control(self, event):
        """
        Very simple joystick control of the sytem
        the left key can control the left motor and on press the value is incremented
        and the right key can control the right motor and on press the value is incremented
        when up arrow is pressed the left motor value is decremented
        when the down arrow is pressed the right motor value is decremented
        Pressing of keyboard will stop the robot also on releasing the keys the values are 
        reset to zero.
        """

        if event.type == pygame.QUIT:
            self._done = True
        
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:

                self._pressed_left = True

            elif event.key == pygame.K_RIGHT:

                self._pressed_right = True

            elif event.key == pygame.K_UP:

                self._pressed_up = True

            elif event.key == pygame.K_DOWN:

                self._pressed_down = True

            elif event.key == pygame.K_SPACE:

                self._rover.stop()

                self._motor_1_cmd, self._motor_2_cmd = 0, 0
        
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:

                self._pressed_left = False

            elif event.key == pygame.K_RIGHT:

                self._pressed_right = False

            elif event.key == pygame.K_UP:

                self._pressed_up = False

            elif event.key == pygame.K_DOWN:

                self._pressed_down = False

        if self._pressed_left:

            self._motor_1_cmd -= self._motor_increment

            self._motor_2_cmd += self._motor_increment

        if self._pressed_right:

            self._motor_1_cmd += self._motor_increment

            self._motor_2_cmd -= self._motor_increment

        if self._pressed_up:

            self._motor_1_cmd += self._motor_increment

            self._motor_2_cmd += self._motor_increment

        if self._pressed_down:

            self._motor_1_cmd -= self._motor_increment

            self._motor_2_cmd -= self._motor_increment

        # if (not self._pressed_left and not self._pressed_up) and (not self._pressed_right and not self._pressed_down):
            
        #     self._motor_2_cmd = 0
            
        #     self._motor_1_cmd = 0


    def draw_robot(self, s):
        """
        The funstion which draws the robot and the laser.
        the input to the function is the current state of the robot
        """
        x,y,th = s[0], s[1], s[2]

        sensed_state = self._rover.sensed_state()

        x_pixel, y_pixel = self.convert_world_to_screen([x], [y])

        robot_surface = pygame.transform.rotate(self._global_robot, th*(180.0/np.pi)%360)

        robot_sensor_surface = pygame.transform.rotate(self._global_robot_sensor_surface, th*(180.0/np.pi)%360)

        new_rect_1 = robot_surface.get_rect(center=(x_pixel[0],y_pixel[0]))

        new_rect_2 = robot_sensor_surface.get_rect(center=(x_pixel[0], y_pixel[0]))

        self._curr_robot_x, self._curr_robot_y = x_pixel, y_pixel

        self._display_screen.blit(robot_surface, new_rect_1)

        self._display_screen.blit(robot_sensor_surface, new_rect_2)

        self._robot_surface = robot_surface

        self._robot_sensor_surface = robot_sensor_surface


    def convert_screen_to_world(self, x_pixel_list, y_pixel_list):
        """
        utility function to converte screen pixel coordinates to the world coordinates
        """
        return [float(x_pixel)/self._ppm for x_pixel in x_pixel_list],\

        [float(self._display_height-y_pixel)/self._ppm for y_pixel in y_pixel_list]
    
    def convert_world_to_screen(self, x_list, y_list):
        """
        utility function to convert world coordinates to screen coordinates.
        """

        return [int(x*self._ppm) for x in x_list], [int(y*self._ppm)  for y in y_list] #+ self._display_height


    # def data_send(self, addData_callbackFunc):

    def show_log(self, status):
        """
        Call back function to denote whether to show the log on the
        screen or not
        """

        self._show_log = status


    def move_own(self, status):
        """
        Call back function to denote whether to move the robot own the
        screen or not
        """

        self._move_own = status


    def run(self, window, plot_data_handle=None):
        """
        The main function that is called intermittently
        by the Qt gui on a timer basis. This function
        takes in the command, makes the robot move forward,
        implements keyboard control, collision checking, shows logs etc.
        Params: window =  type qt screen which takes in input to draw robot
        """

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                return True

            self.key_board_menu_control(event)

        if self._move_own:

            self._motor_1_cmd, self._motor_2_cmd = np.random.randn(2)

        if self.collision_check():

            curr_x = self._rover.true_state()
            
            self._rover.stop()
            
            self._motor_1_cmd, self._motor_2_cmd = -self._motor_1_cmd, -self._motor_2_cmd

            slope = np.arctan2( (curr_x[1]-3.5), (curr_x[0]-2.) )

            self._rover.reset([curr_x[0]-0.2*np.cos(slope), curr_x[1]-0.2*np.sin(slope), curr_x[2]])

            logging.info("Collision Detected! Moving back....")

        self._display_screen.fill(self._bg_color)

        true_state   =  self._rover.command_robot(np.array([self._motor_1_cmd, self._motor_2_cmd]))
        
        sensed_state = self._rover.sensed_state()

        if self._show_log:

            logging.info("*********Start*********")

            for key in sensed_state:

                logging.info(key + '\t{}\t'.format(str(sensed_state[key])))

            logging.info("*********End*********")

        self.draw_robot(true_state)

        if plot_data_handle is not None:

            plot_data_handle(sensed_state['Encoder'])

        self._all_sprites_list.draw(self._display_screen)
        
        pygame.display.flip()

        self._clock.tick(self._fps)

        return False

        
