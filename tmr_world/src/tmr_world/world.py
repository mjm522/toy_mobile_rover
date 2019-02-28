import thorpy
import pygame
import logging
import numpy as np
from sprites import Wall, Agent


class World():

    def __init__(self, rover_interface, config=None):

        self._fps = config['FPS']

        self._ppm = config['PPM']

        self._bg_color = config['bg_color']

        self._laser_color = config['laser_color']

        self._robot_color = config['robot_color']

        self._display_width = config['screen_width']

        self._display_height  = config['screen_height']

        self._motor_increment = config['motor_increment']

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

                self._wall_list .add(block)

                self._all_sprites_list.add(block)


    def init_robot(self):
        return
        self._robot_sprite = Agent(self._robot_color,  70,  55)

        self._all_sprites_list.add(self._robot_sprite)

            
    def key_board_menu_control(self):
        """
        Very simple joystick control of the sytem
        the left key can control the left motor and on press the value is incremented
        and the right key can control the right motor and on press the value is incremented
        when up arrow is pressed the left motor value is decremented
        when the down arrow is pressed the right motor value is decremented
        Pressing of keyboard will stop the robot also on releasing the keys the values are 
        reset to zero.
        """

        for event in pygame.event.get():

            # self._menu.react(event)

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

        if (not self._pressed_left and not self._pressed_up) and (not self._pressed_right and not self._pressed_down):
            
            self._motor_2_cmd = 0
            
            self._motor_1_cmd = 0


    def draw_robot(self, s):
        """
        The funstion which draws the robot and the laser.
        the input to the function is the current state of the robot
        """
        x,y,th = s[0], s[1], s[2]

        sensed_state = self._rover.sensed_state()
        # laser_corners = sensed_state['ultrasound']

        x_pixel, y_pixel = self.convert_world_to_screen([x], [y])
        

        # self._robot_sprite.update(x_pixel[0], y_pixel[0], (th/np.pi)*180)
        # self._robot_sprite.rect.x=x_pixel[0]
        # self._robot_sprite.rect.y=y_pixel[0]

        rot_mat = self._rover.compute_rot_mat()

        fwd_corners = rot_mat.dot(np.array([[0., 1., 1., 0.], 
                                            [-0.1, -0.1, 0.1, 0.1] ]))

        fwd_x_pixel, fwd_y_pixel = self.convert_world_to_screen(fwd_corners[0,:]+x, fwd_corners[1,:]+y)


        pygame.draw.circle(self._display_screen, self._laser_color, [ x_pixel[0], y_pixel[0] ], 150, 0)

        pygame.draw.circle(self._display_screen, self._robot_color, [ x_pixel[0], y_pixel[0] ], 100, 0)

        pygame.draw.circle(self._display_screen, self._robot_color, [ x_pixel[0], y_pixel[0] ], 100, 0)

        pygame.draw.polygon(self._display_screen, (0,0,255,255), [[l_x, l_y] for l_x, l_y in zip(fwd_x_pixel, fwd_y_pixel) ] , 2)


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


    def run(self):

        """
        The main function that runs the
        demo
        """

        logging.getLogger().setLevel(logging.INFO)

        while not self._done:

            self.on_exit()

            self._display_screen.fill(self._bg_color)

            self.key_board_menu_control()

            true_state =  self._rover.command_robot([self._motor_2_cmd, self._motor_1_cmd])
            
            sensed_state = self._rover.sensed_state()

            logging.info(sensed_state['time']+'ENCODER READING'+np.array2string(sensed_state['encoder']))
            
            logging.info(sensed_state['time']+'ULTRASONIC READING'+np.array2string(sensed_state['ultrasonic']))

            self.draw_robot(true_state)

            self._all_sprites_list.draw(self._display_screen)
            
            pygame.display.flip()

            self._clock.tick(self._fps)

        
