import unittest
import numpy as np
from tmr_sensors.laser.laser import Laser
from tmr_sensors.encoder.encoder import Encoder
from tmr_robot.config import MOBILE_ROVER_CONFIG
from tmr_sensors.laser.config import LASER_CONFIG
from tmr_sensors.encoder.config import ENCODER_CONFIG


class TestRover(unittest.TestCase):

    def test(self):
        las = Laser(LASER_CONFIG)
        enc = Encoder(ENCODER_CONFIG)
        self.assertEqual(len(las.reading()), 6)
        self.assertEqual(len(enc.reading() ), 6)


def main():
    unittest.main()

if __name__ == "__main__":
    main()