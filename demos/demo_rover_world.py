import sys
import numpy as np
from tmr_gui.gui import GUI
from tmr_rover.rover import Rover
from tmr_world.world import World
from PyQt5.QtWidgets import QApplication
from tmr_world.config import WORLD_CONFIG
from tmr_rover.config import ROVER_CONFIG

np.random.seed(123)

def main():
    
    rover_world = World(rover_interface=Rover(config=ROVER_CONFIG), config=WORLD_CONFIG)
    
    app = QApplication(sys.argv)
    
    ex = GUI(rover_world, ROVER_CONFIG)
    
    result = app.exec_()

    print("TMR rover demo finished: " + str(result))
    
    sys.exit(result)

if __name__ == "__main__":

    main()
