# ASCENT Robotics - Code Asignment - Sensor System

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

The system in this file consists of a small toy robot in a world. The robot consists of two sensors, ultrasonic sensor and an encoder. Adding any more sensors is trivial by adding additional modules in the tmr_sensors>src>tmr_sensors. The robot moves in the world by using the arrow keys. The robots position is updated using Runge-Kutta 4rth order integration. The step size and the integral time constant can be modified by changing parameters in the tmr_robot>config file. The system currently loggs in values on the screen. 

## 4 Setup instructions

    Run $./install_dependencies.sh

    Now we need to setup the PYTHONPATH. The modules of the library can be installed, but for the testing, just source the following file.

    Run $source setup_tmr.bash

    The mobile rover seen can be controlled using the arrow keys.

    At present, two sensors are implemented, scaling this platform up is quite trivial.

    To change parameters of the sensors, change values in tmr_sensors>src>tmr_sensors>encoder>config

    To change parameters of the sensors, change values in tmr_sensors>src>tmr_sensors>ultrsonic>config

### 5 Optional steps

    To generate documentation of the library install doxygen by type in doxygen doxygen_config_file

### 6 To Fix
    
    The gui needs to be fixed for making the config file run time configurable. 

    To fix the collision detection

    To add plotting windows on seperate threads to show the readings.

