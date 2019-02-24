import numpy as np
from tmr_robot.robot import Robot
from tmr_sensors.laser.laser import Laser
from tmr_sensors.encoder.encoder import Encoder
from tmr_robot.config import MOBILE_ROVER_CONFIG
from tmr_sensors.laser.config import LASER_CONFIG
from tmr_sensors.encoder.config import ENCODER_CONFIG

class Rover():

    def __init__(self):

        self._robot = Robot(robot_config)
        self._robot.init_start(x0=0., y0=0., alpha0=0.)
        self._encoder = Encoder(self._robot, encoder_config)
        self._laser = Laser(self._robot, laser_config)


    def state(self):

        robot_state = {
        'ecoder':self._encoder.reading(),
        'laser':self._laser.reading(),
        # 'pose':self.pose()
        }

    # def pose(self):

    #     e_r, e_l = self._encoder.reading()

        
