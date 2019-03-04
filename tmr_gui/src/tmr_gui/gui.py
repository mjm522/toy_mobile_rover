import sys, time
import threading
from functools import partial
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import QTimer, QRect
from tmr_gui.configure_popup import ConfigurePopup
from tmr_gui.embed_plot import EmbedPlot, Communicate
from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QFrame, QGridLayout


class GUI(QWidget):

    def __init__(self, rover_world, rover_config):

        super().__init__()
        
        self._title = 'TMR Control Panel'

        self._left = 0
        
        self._top = 0
        
        self._width = 800
        
        self._height = 540

        self._sensor_configs = [sensor.config() for sensor in rover_config['sensors']]

        self._robot_config = rover_world._rover._robot.config()
        
        self.init_ui()
        
        self.init_pygame(rover_world)
 
    def init_ui(self):
        
        self.setWindowTitle(self._title)
        
        self.setGeometry(self._left, self._top, self._width, self._height)

        self._s_button = QPushButton('Configure Sensors', self)

        self._r_button = QPushButton('Configure Robot', self)
        
        self._s_button.move(540, 100)
        
        self._r_button.move(550, 200)

        self._s_button.clicked.connect(self.drop_down)

        self._r_button.clicked.connect(partial(self.pop_up, None))

        self.init_plot()        

        self.show()

    def init_plot(self):

        self._frame = QFrame(self)
        
        self._frame.setStyleSheet("QWidget { background-color: %s }" % QColor(210,210,235,255).name())
        
        self._layout = QGridLayout()
        
        self._frame.setLayout(self._layout)
    
        # Place the matplotlib figure
        self._canvas = EmbedPlot()

        self._layout.addWidget(self._canvas, *(0,1))

        # data_loop = threading.Thread(name = 'tmr_data_loop', target=self._canvas.data_receiver, daemon = True, args = (self.plot_data,))
        
        # data_loop.start()

    def plot_data(self, d):

        self._canvas.add_data(d)


    def drop_down(self):

        self._sensor_list = QComboBox(self)

        for idx, sensor in enumerate(self._sensor_configs):

            self._sensor_list.addItem(sensor['name'])

            self._sensor_list.activated[str].connect(partial(self.pop_up, idx))

        self._sensor_list.move(3*self._width/4, self._height/2)

        self._sensor_list.show()

    def pop_up(self, sensor_idx):
        
        self._sensor_config = ConfigurePopup(self, sensor_idx)

        self._sensor_config.move(self._width/2, self._height/2)

        self._sensor_config.show()

        if sensor_idx is not None:

            self._sensor_list.close()

    def robot_config(self):
        return self._robot_config

    def config_at_idx(self, idx):

        return self._sensor_configs[idx]

    def update_configs(self, vals, idx):

        if idx is None:
            self._robot_config['params'].update({k : vals[i] for i,k in enumerate(self._robot_config['params'].keys())})
            self._rover_world.update_robot_config(self._robot_config)
        else:
            self._sensor_configs[idx]['params'].update({k : vals[i] for i,k in enumerate(self._sensor_configs[idx]['params'].keys())})
            self._rover_world.update_sensor_config(self._sensor_configs[idx], idx)
     
    def init_pygame(self, rover_world):
        
        self._rover_world = rover_world

        self._timer = QTimer()

        self._timer.timeout.connect(self.pygame_loop)

        self._timer.start(0)

    def pygame_loop(self):

        if self._rover_world.run(self, self.plot_data):

            self.close()


# def dataSendLoop(addData_callbackFunc):
#     # Setup the signal-slot mechanism.
#     mySrc = Communicate()
#     mySrc.data_signal.connect(addData_callbackFunc)

#     # Simulate some data
#     n = np.linspace(0, 499, 500)
#     y = 50 + 25*(np.sin(n / 8.3)) + 10*(np.sin(n / 7.5)) - 5*(np.sin(n / 1.5))
#     i = 0

#     while(True):
#         if(i > 499):
#             i = 0
#         time.sleep(0.1)
#         mySrc.data_signal.emit(y[i]) # <- Here you emit a signal!
#         i += 1
