import unittest
import numpy as np
from tmr_robot.robot import Robot
from tmr_robot.config import MOBILE_ROVER_CONFIG


class TestRobot(unittest.TestCase):

    def test(self):

        rbt = Robot(MOBILE_ROVER_CONFIG)
        rbt.init_start(x0=0., y0=0., alpha0=0.)
        u = np.zeros(2)
        self.assertEqual(len(rbt.step(u)), 6)


def main():
    unittest.main()

if __name__ == "__main__":
    main()


