import unittest
import numpy as np
from tmr_rover.rover import Rover
from tmr_rover.config import ROVER_CONFIG

class TestRover(unittest.TestCase):

    def test(self):
        rov = Rover(config=ROVER_CONFIG)
        self.assertEqual(len(rov._robot.step(np.random.randn(2))), 6)


def main():
    unittest.main()

if __name__ == "__main__":
    main()