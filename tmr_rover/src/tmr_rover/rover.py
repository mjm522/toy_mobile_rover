import datetime

class Rover():

    def __init__(self, config):
        """
        The class which combines the robot with the sensors.
        """

        self._robot = config['robot']

        self._robot.init_start(x0=2.0, y0=3.5, alpha0=0.)

        self._sensors = config['sensors'] 

    def command_robot(self, u):
        """
        The function that sends commnads to the robto
        inputs : u = control commands of the left and right wheel
        """

        true_state = self._robot.step(u)

        for sensor in self._sensors:
            sensor.update()

        return true_state

    def stop(self):
        """
        The utility function to insteneously stop the robot
        """

        self._robot.stop()

    def sensed_state(self):
        """
        This the key dictionary of values
        It contains the sensor readings of all the sytems in place
        """
        robot_state = {'time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        for sensor in self._sensors:
            robot_state[sensor.name()]=sensor.reading()

        return robot_state

    def compute_rot_mat(self):
        """
        utility funciton to compute the current rotation
        matrix of the robot
        """

        return self._robot.compute_rot_mat()
