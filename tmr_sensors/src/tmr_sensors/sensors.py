import abc

class Sensors(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, robot_interface, config):

        self.init_sensor(config)

        self._curr_value = None

        self._robot = robot_interface
        
        self.disable()


    def init_sensor(self, config):

        self._config = config

        self._name = config['name']

        self._res = config['params']['res']

        self._noise_gain = config['params']['noise_gain']

        self._noise_type = config['noise_type']

        self._range = config['params']['range']


    @abc.abstractmethod
    def update(self):

        raise NotImplementedError("Must be implemented in the subclass")

    @abc.abstractmethod
    def reset(self):

        raise NotImplementedError("Must be implemented in the subclass")


    @abc.abstractmethod
    def noise(self):

        raise NotImplementedError("Must be implemented in the subclass")


    def config(self):
        return self._config

    def name(self):
        return self._name

    def reading(self):

        return self._curr_value

    def enable(self):

        self._is_active = True

    def disable(self):

        self._is_active = False
