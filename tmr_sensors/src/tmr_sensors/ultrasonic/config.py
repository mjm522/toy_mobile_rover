from tmr_robot.config import MOBILE_ROVER_CONFIG

ULTRASONIC_CONFIG={
    'res':0.001, #
    'noise_gain':0.001, #noise gain
    'noise_type':'random',
    'range':2.,
    'beam_radius':MOBILE_ROVER_CONFIG['robot_r']*2.,
    'map_config':None,
}
