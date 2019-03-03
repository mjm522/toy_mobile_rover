from tmr_robot.robot import Robot
from tmr_world.config import WORLD_CONFIG
from tmr_sensors.encoder.encoder import Encoder
from tmr_robot.config import MOBILE_ROVER_CONFIG
from tmr_sensors.encoder.config import ENCODER_CONFIG
from tmr_sensors.ultrasonic.ultrasonic import Ultrasonic
from tmr_sensors.ultrasonic.config import ULTRASONIC_CONFIG

ULTRASONIC_CONFIG['obstacle_config'] = WORLD_CONFIG['obstacle_config']

robot = Robot(MOBILE_ROVER_CONFIG)

ROVER_CONFIG = {
    'robot':robot,
    'sensors':[Encoder(robot, ENCODER_CONFIG), Ultrasonic(robot, ULTRASONIC_CONFIG)],
}