import os
import copy
import pygame
import logging
import numpy as np
from math import fabs
from tmr_world.sprites import Wall, Agent


class World():

    def __init__(self, rover_interface, config):

        self._fps = config['FPS']

        self._ppm = config['PPM']

        self._bg_color = config['bg_color']

        self._laser_color = config['laser_color']

        self._laser_alpha = config['laser_alpha']

        self._robot_color = config['robot_color']

        self._display_width = config['screen_width']

        self._display_height  = config['screen_height']

        self._motor_increment = config['motor_increment']

        self._laser_sensor_idx = config['laser_sensor_idx']

        self._rover = rover_interface

        self._done = False

        self._motor_1_cmd = 0.

        self._motor_2_cmd = 0.

        pygame.init()

        self._clock = pygame.time.Clock()

        self._font = pygame.font.SysFont(None, 25)
        
        self._display_screen = pygame.display.set_mode((self._display_width, self._display_height))

        pygame.display.set_caption('Toy Mobile Rover')

        self.init_map(config['map_config'])

        self.init_robot()

        self.init_keyboard_ctrl()


    def init_keyboard_ctrl(self):

        self._pressed_up =  False

        self._pressed_down =  False

        self._pressed_left =  False

        self._pressed_right =  False


    def init_map(self, map_config):

        if map_config is None:
            return
        
        self._wall_list = pygame.sprite.Group()

        self._all_sprites_list = pygame.sprite.Group()

        if map_config['wall_corners'] is not None:

            for l, s in zip(map_config['wall_corners'], map_config['wall_size']):

                block = Wall(map_config['wall_color'], s[0], s[1])

                block.rect.x = l[0]

                block.rect.y = l[1]

                self._wall_list .add(block)

                self._all_sprites_list.add(block)

        if map_config['obstacles_locations'] is not None:

            for l, s in zip(map_config['obstacles_locations'], map_config['obstacles_size']):

                # This represents a block
                block = Wall(map_config['obstacle_color'], s[0], s[1])

                block.rect.x = l[0]

                block.rect.y = l[1]

                self._wall_list.add(block)

                self._all_sprites_list.add(block)


    def update_sensor_config(self, new_sensor_config, idx):

        self._rover.update_sensor_config(new_sensor_config, idx)

        self.init_robot()

    def update_robot_config(self, new_robot_config):

        self._rover.update_robot_config(new_robot_config)

        self.init_robot()

    def has_collided_with(self,  mob, player):
        if mob.rect.right > player.left and \
           mob.rect.left < player.right and \
           mob.rect.bottom > player.top and \
           mob.rect.top < player.bottom:
               collide = True
               print("sdfhakdjfalkfjn")
        # deltay = fabs(rect1.centery - rect2.centery)
        # deltax = fabs(rect1.centerx - rect2.centerx)
        # print(deltay < rect2.height and deltax < rect2.width)
        # return deltay < rect2.height and deltax < rect2.width

    def collision_check(self):
        return

        for block in self._wall_list:
            
            if self.has_collided_with( block, self._robot_surface.get_rect()):
                
                new_rect_1 = self._robot_surface.get_rect(center=(self._display_width/2, self._display_height/2))
                
                self._display_screen.blit( new_rect_1, self._robot_surface)



    def init_robot(self):

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

            self._motor_1_cmd += self._motor_increment

            self._motor_2_cmd -= self._motor_increment

        if self._pressed_right:

            self._motor_1_cmd -= self._motor_increment

            self._motor_2_cmd += self._motor_increment

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


    def run(self, window, plot_data_handle=None):

        logging.getLogger().setLevel(logging.INFO)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                return True

            self.key_board_menu_control(event)

        self._display_screen.fill(self._bg_color)

        true_state =  self._rover.command_robot(np.array([self._motor_2_cmd, self._motor_1_cmd]))
        
        sensed_state = self._rover.sensed_state()

        self.collision_check()

        # print (sensed_state)

        # print (self._motor_1_cmd, self._motor_2_cmd)

        # print (sensed_state)

        self.draw_robot(true_state)

        if plot_data_handle is not None:
            plot_data_handle(sensed_state['Encoder'])

        self._all_sprites_list.draw(self._display_screen)
        
        pygame.display.flip()

        self._clock.tick(self._fps)

        return False

        
