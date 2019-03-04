PPM = 100
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1024
WALL_WIDTH = 15
from tmr_world.utils import make_obstacle_world


MAP_CONFIG={
    'wall_color':(255,255,255),
    'obstacle_color':(125,125,125),
    'wall_corners':[ [0,0], [0, SCREEN_HEIGHT-WALL_WIDTH], [0, 0],  [SCREEN_WIDTH-WALL_WIDTH ,0] ],
    'wall_size':[[SCREEN_WIDTH,WALL_WIDTH], [SCREEN_WIDTH, WALL_WIDTH], [WALL_WIDTH,SCREEN_HEIGHT], [WALL_WIDTH, SCREEN_HEIGHT]],
    'obstacles_locations':[[int(0.75*SCREEN_WIDTH), int(0.75*SCREEN_HEIGHT)], [int(0.25*SCREEN_WIDTH),  0]],
    'obstacles_size':[[ WALL_WIDTH, int(0.25*SCREEN_HEIGHT) ], [ WALL_WIDTH, int(0.25*SCREEN_HEIGHT) ] ],
}


WORLD_CONFIG={
    'laser_alpha':128,
    'robot_color':(0,155,0,0),
    'laser_sensor_idx':1,
    'laser_color':(125,125,125,0),
    'screen_height':SCREEN_HEIGHT,
    'screen_width':SCREEN_WIDTH,
    'PPM':PPM,
    'FPS':10,
    'bg_color':(0,0,0),
    'line_color':(255, 0, 0),
    'line_thickness':5,
    'motor_increment':0.1,
    'map_config':MAP_CONFIG,
    'obstacle_config':make_obstacle_world(MAP_CONFIG, PPM, SCREEN_HEIGHT),
}