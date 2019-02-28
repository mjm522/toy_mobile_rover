import numpy as np
from tmr_rover.rover import Rover
from tmr_world.world import World
from tmr_world.config import WORLD_CONFIG



def main():

    rover_world = World(rover_interface=Rover(), config=WORLD_CONFIG)
    
    rover_world.run()


if __name__ == '__main__':
    main()