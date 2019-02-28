import datetime
import numpy as np
from tmr_robot.robot import Robot
from tmr_world.config import WORLD_CONFIG
from tmr_sensors.encoder.encoder import Encoder
from tmr_robot.config import MOBILE_ROVER_CONFIG
from tmr_sensors.encoder.config import ENCODER_CONFIG
from tmr_sensors.ultrasonic.ultrasonic import Ultrasonic
from tmr_sensors.ultrasonic.config import ULTRASONIC_CONFIG

class Rover():

    def __init__(self):
        """
        The class which combines the robot with the sensors.
        """

        self._robot = Robot(config=MOBILE_ROVER_CONFIG)

        self._robot.init_start(x0=2.0, y0=3.5, alpha0=0.)

        self._encoder = Encoder(robot_interface=self._robot, config=ENCODER_CONFIG)

        ULTRASONIC_CONFIG['obstacle_config'] = WORLD_CONFIG['obstacle_config']

        self._ultra_sonic = Ultrasonic(robot_interface=self._robot, config=ULTRASONIC_CONFIG)

    def command_robot(self, u, world_state=None):
        """
        The function that sends commnads to the robto
        inputs : u = control commands of the left and right wheel
        """

        true_state = self._robot.step(u)

        self._encoder.update()

        self._ultra_sonic.update(world_state)

        return true_state

    def stop(self):
        """
        The utility function to insteneously stop the robot
        """

        self._robot.stop()

    def sensed_state(self):
        """
        This the key dictionary of values
        It contains the sensor readings of all the sytems in place
        """

        robot_state = {
        'time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'encoder':self._encoder.reading(),
        'ultrasonic':self._ultra_sonic.reading(),
        }

        return robot_state

    def compute_rot_mat(self):
        """
        utility funciton to compute the current rotation
        matrix of the robot
        """

        return self._robot.compute_rot_mat()
