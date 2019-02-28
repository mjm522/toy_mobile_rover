import numpy as np

def convert_screen_to_world(screen_x, screen_y, ppm, screen_ht):
    """
    utility function to converte screen pixel coordinates to the world coordinates
    """
    return np.array([float(screen_x)/ppm , float(screen_ht-screen_y)/ppm])


def make_obstacle_world(map_config, ppm, screen_ht):

    map_obstacles_start = []
    map_obstacles_end = []

    if map_config['wall_corners'] is not None:
        for l, s in zip(map_config['wall_corners'], map_config['wall_size']):

            map_obstacles_start.append(convert_screen_to_world(l[0], l[1], ppm, screen_ht ))
            map_obstacles_end.append(convert_screen_to_world(s[0], s[1], ppm, screen_ht ))


    if map_config['obstacles_locations'] is not None:
        for l, s in zip(map_config['obstacles_locations'], map_config['obstacles_size']):

            map_obstacles_start.append(convert_screen_to_world(l[0], l[1], ppm, screen_ht) )
            map_obstacles_end.append(convert_screen_to_world(s[0], s[1], ppm, screen_ht ))

    return {'obstacles_start':map_obstacles_start, 'obstacles_end':map_obstacles_end}