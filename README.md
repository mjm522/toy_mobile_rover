
# Sensor System - A Toy System

In this project you will be implementing a (very simple) simulated sensor system. You will need to come up with a few different types of sensors, create a prototype of them and build a system using them.

## 1 Sensor System Implementation

Expected implementation time: 2-4 hours

A robot moving in the real world processes a vast amount of sensory information. You need to create a simple, abstract robot system with its abstract sensor loadout and perform some kind of runtime test (or task) with this system.

Feel free to forget about the robotics and control parts of this problem, this is a pure software engineering assignment. Come up with a framework that is extendable and maintainable and has the potential to handle several sensor models connected into a network.

There is no need for visualization and there is also no need to collect real data (but you can
do it if you would like to).

### Requirements

    • Create a simple sensory framework or platform
    • Create several dummy sensors (at least a few di↵erent types)
    • Create a run environment that starts the platform and the sensors
    • Send some data between the sensors or between the sensor and the platform or both
    (no need to process data)
    • Come up with a run test that demonstrates data flowing through the system (for
    example via logs or status messages or maybe visualization)
    • Bonus points if you make the whole system runtime configurable

### Notes

Your submission doesn’t have to be super complicated! Feel free to use any existing libraries but it is also encouraged to create your (simple) framework from scratch. Also, your ”sensors” can be arbitrary, made-up, abstract models - no need to mimic existing sensors or datatypes. This more about principles and design and not about real world simulation.

## 2 Submission

### Compilation and running instructions

Since this is an open ended task and you can come up with all kinds of things, be sure to take extra care providing us with usage instructions. If we will not be able to run your code or reproduce your results, that will shine a bad light on you.

## 3 Brief Description

The system in this file consists of a small toy robot in a world. The robot consists of two sensors, ultrasonic sensor and an encoder. Adding any more sensors is trivial by adding additional modules in the tmr_sensors>src>tmr_sensors. The robot moves in the world by using the arrow keys or by own. If the Move Own check box in the GUI is checked, then the robot is given random control commands. In case the robot needs to be controlled via the keyboard this checkbox needs to be unchecked. The robots position is updated using Runge-Kutta 4rth order integration. The step size and the integral time constant can be modified by changing parameters in the tmr_robot>config file.  By adding more sensors, the Gui can automatically adapt the number of new sensors added.  The GUI window offers facility to change the configuration of the sensors and the robot. The parameters can be changed and instantly the visualization can be seen of the screen. If the values are to be logged then the checkbox in the GUI can be checked. The visualizer provided can log the values of different sensors depending on whether sensor gives a type of plottable values. This plotability of a sensor can be configured in the corresponding config file. 

![Alt text](https://img.youtube.com/vi/7oLWn1YgTRc/0.jpg)](https://www.youtube.com/watch?v=7oLWn1YgTRc)


## 4 Requirment Analysis

    • Create a simple sensory framework or platform

   The whole tmr_sensor is the sensory framework consisting of the sensor modules. The newer version of the sensors can be added more to this module. The whole set of sensors are integrated to a toy robot module from tmr_robot and kept in the tmr_rover module. Every modification to the system can be changed by modifying the single config file seen in the tmr_rover>config file


    • Create several dummy sensors (at least a few di↵erent types)

   At present two sensors are added (Encoder and Ultrasonic). Adding more sensor is trivial. One needs to create child classes of tmr_sensor>sensor. Once the new sensor is created it can be added to the system by just simply modifying the tmr_rover>config file. 

    • Create a run environment that starts the platform and the sensors

   The tmr_world is the environment which runs the tmr_rover module. The tmr_rover is a combination of tmr_robot and tmr_sensors. The world consists of a map which can be added with more obstacles by modifying the tmr_world>config file. 
   The world file also gives options to interact with the robot randomly.

    • Send some data between the sensors or between the sensor and the platform or both
    (no need to process data)

   The data flow can be seen in two ways. Through the plot window present in the GUI. The plottable values of the sensor are available from the GUI. Also the log of the sensor readings can be clicking the chek box. 

    • Come up with a run test that demonstrates data flowing through the system (for
    example via logs or status messages or maybe visualization)

This is the file which is the demo>demo_rover_world.py

    • Bonus points if you make the whole system runtime configurable

   The whole sesnor and robot system is online configurable by playing with different values in via the GUI.


## 5 Setup instructions (Tested with Python 3.5 on Ubuntu 16.04)

Ideally it is recommended to create a virtual environment to test this system. Make sure to create one using Python3. It can be done as follows. It is assumed you have installed virutalenvironment wrapper.

    $ which python3 #Output: /usr/bin/python3

    $ mkvirtualenv --python=/usr/bin/python3 nameOfEnvironment

Clone the github repository to a suitable location

    $ git clone https://github.com/mjm522/toy_mobile_rover


Setup the dependencies. For that, run following in the terminal

    $ ./install_dependencies.sh

   Now we need to setup the PYTHONPATH. The modules of the library can be installed, but for the testing, just source the following file.

    $ source setup_tmr.bash

   Check the demo by running,
     
    $ python demos/demo_rover.world.py

The mobile rover seen can be controlled using the arrow keys once the pygame window is selected. At present, two sensors are implemented, scaling this platform up is quite trivial. To change parameters of the sensors, change values by clicking the GUI button sensor config
The gui has been written in a way to scale arbitarily to any number of sensors.

### 6 Optional steps

To generate documentation of the library install doxygen by type in 
    
    $ doxygen doxygen_config_file

### 7 To Fix 

    Perfect the collision detection slightly more. 

    To improve the test cases.

    

