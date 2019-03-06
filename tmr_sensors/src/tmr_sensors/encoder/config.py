
PARAMS = {
    'res':0.01, #
    'noise_gain':0.001, #noise gain
    'range':6.28,
}


ENCODER_CONFIG={
    'name':'Encoder',
    'noise_type':'random',
    'params':PARAMS,
    'val_dim':2,
    'plotable_vals':{'left_wheel':0, 'right_wheel':1},
    'precision':3,
}
