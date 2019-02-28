import numpy as np

def sigmoid(x):
    
  return 1. / (1. + np.exp(-x))

def rk4_average(x):

    x_i, k1, k2, k3, k4 = x

    return x_i + (k1 + 2.0*(k3 + k4) +  k2) / 6.0

def gaussian(x, mu, sig):

    return np.exp(-np.power(x - mu, 2.) / (2.*np.power(sig, 2.)))

def check_random_state(seed):
    """Turn seed into a np.random.RandomState instance
    If seed is None, return the RandomState singleton used by np.random.
    If seed is an int, return a new RandomState instance seeded with seed.
    If seed is already a RandomState instance, return it.
    Otherwise raise ValueError.
    """
    if seed is None or seed is np.random:

        return np.random.mtrand._rand

    if isinstance(seed, (numbers.Integral, np.integer)):

        return np.random.RandomState(seed)

    if isinstance(seed, np.random.RandomState):

        return seed

    raise ValueError('%r cannot be used to seed a numpy.random.RandomState'
                     ' instance' % seed)