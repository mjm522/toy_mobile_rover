from tmr_robot.config import MOBILE_ROVER_CONFIG

PARAMS = {
    'res':0.001, #
    'noise_gain':0.001, #noise gain
    'range':2,
}

ULTRASONIC_CONFIG={
    'name':'Ultrasonic',
    'noise_type':'random',
    'map_config':None,
    'params':PARAMS,
    'val_dim':None,
    'plotable_vals':None,
    'obstacle_config':None,
    'precision':3,
}
