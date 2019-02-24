import unittest
import numpy as np
from tmr_rover.rover import Rover


class TestRover(unittest.TestCase):

    def test(self):
        rov = Rover()
        self.assertEqual(len(rov.step(u)), 6)


def main():
    unittest.main()

if __name__ == "__main__":
    main()