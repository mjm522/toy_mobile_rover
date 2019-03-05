import unittest
import numpy as np
from tmr_robot.robot import Robot
from tmr_sensors.encoder.encoder import Encoder
from tmr_robot.config import MOBILE_ROVER_CONFIG
from tmr_sensors.encoder.config import ENCODER_CONFIG
from tmr_sensors.ultrasonic.ultrasonic import Ultrasonic
from tmr_sensors.ultrasonic.config import ULTRASONIC_CONFIG


class TestRover(unittest.TestCase):

    def test(self):

        robot = Robot(MOBILE_ROVER_CONFIG)

        las = Ultrasonic(robot, ULTRASONIC_CONFIG)

        enc = Encoder(robot, ENCODER_CONFIG)

        self.assertEqual(len(las.reading()),  1)
        
        self.assertEqual(len(enc.reading() ), 2)


def main():
    unittest.main()

if __name__ == "__main__":
    main()