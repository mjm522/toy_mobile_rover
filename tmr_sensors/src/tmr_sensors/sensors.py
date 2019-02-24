import abc

class Sensors(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, robot_interface, config):
        self._config = config
        self._curr_value = None
        self._robot = robot_interface
        self._res = config['res']
        self._noise_gain = config['noise_gain']
        self._noise_type = config
        self.disable()


    @abc.abstractmethod
    def update(self):
        raise NotImplementedError("Must be implemented in the subclass")


    def reading(self):
        return self._curr_value

    @abc.abstractmethod
    def reset(self):
        raise NotImplementedError("Must be implemented in the subclass")


    def enable(self):
        self._is_active = True

    def disable(self):
        self._is_active = False
