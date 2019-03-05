#!/usr/bin/env python3
"""Provides GUI which creates the control panel for the tmr robot.
The class provides a fully extendable ways to add popups, more buttons
and other windows to provide capability to plot sensor readinds,
configure the sensors etc.

Copyright (C) 2019 Michael J Mathew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

__author__     = "Michael J Mathew"
__copyright__  = "Copyright 2019, The Ascent Project"
__license__    = "GNU"
__version__    = "0.0.0"
__maintainer__ = "Michael J Mathew"
__email__      = "mjm522@student.bham.ac.uk"
__status__     = "Development"

import sys, time
import threading
from functools import partial
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import QTimer, QRect, Qt
from tmr_gui.configure_popup import ConfigurePopup
from tmr_gui.embed_plot import EmbedPlot, Communicate
from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QFrame, QGridLayout, QLabel, QMessageBox, QCheckBox


class GUI(QWidget):

    def __init__(self, rover_world, rover_config):

        """
        Constructor of the class
        Params: rover_world : object of type tmr_world.world
                rover_config: params of the tmr_rover.rover
        """

        super().__init__()
        
        self._title          = 'TMR Control Panel'

        self._left           = 0
        
        self._top            = 0
        
        self._width          = 800
        
        self._height         = 540

        self._sensor_configs = [sensor.config() for sensor in rover_config['sensors']]

        self._robot_config   = rover_world._rover._robot.config()
        
        self.init_ui()
        
        self.init_pygame(rover_world)
 
    def init_ui(self):
        """
        Initialse basic Gui. It contains three buttons
        at hard coded locations. The locations of the buttons can be 
        made as a parameter, but since our gui is fixed in size
        it doesn't matter much. 
        """
        
        self.setWindowTitle(self._title)
        
        self.setGeometry(self._left, self._top, self._width, self._height)

        self._s_button = QPushButton('Configure Sensors', self)

        self._r_button = QPushButton('Configure Robot', self)

        self._v_button = QPushButton('Configure Visuals', self)
        
        self._s_button.move(540, 100)
        
        self._r_button.move(550, 200)

        self._v_button.move(550, 300)

        self._s_button.clicked.connect(partial(self.drop_down, 'edit'))

        self._r_button.clicked.connect(partial(self.pop_edit_up, None))

        self._v_button.clicked.connect(partial(self.drop_down, 'check'))

        self._move_check_box = QCheckBox("Self Move", self)

        self._log_check_box = QCheckBox("Print Log", self)

        self._log_check_box.move(550, 400)

        self._move_check_box.move(550, 450)

        self._move_check_box.setChecked(True)

        self._log_check_box.stateChanged.connect(self.update_log_status)

        self._move_check_box.stateChanged.connect(self.update_move_status)

        self.init_plot()   

        self.show()

        self.show_initial_info()


    def init_plot(self):
        """
        Creates the plot window in the qt panel
        Plots only one value at a time.
        The value to be plotted can be chosen from the panel
        """

        self._frame = QFrame(self)
        
        self._frame.setStyleSheet("QWidget { background-color: %s }" % QColor(210,210,235,255).name())
        
        self._layout = QGridLayout()

        self._plot_status = {}

        self._plot_defualt_idx = None

        for idx, config in enumerate(self._sensor_configs):

            if config['plotable_vals'] is not None:

                if self._plot_defualt_idx is None:

                    self._plot_defualt_idx = idx

                self._plot_status[idx] = [False for _ in range(len(config['plotable_vals']))]

        if self._plot_defualt_idx is not None:

            self._plot_status[self._plot_defualt_idx][0] = True

        self._frame.setLayout(self._layout)
    
        self._canvas = EmbedPlot()

        self._layout.addWidget(self._canvas, *(0,1))

        # data_loop = threading.Thread(name = 'tmr_data_loop', target=self._canvas.data_receiver, daemon = True, args = (self.plot_data,))
        
        # data_loop.start()


    def show_initial_info(self):
        """
        A dialog box to give initial information
        on how to control the system.
        """

        msg = QMessageBox()
        
        msg.setIcon(QMessageBox.Information)

        msg.setText("Use the arrow keys intermittently to move robot after selecting the rover window")
        
        msg.setInformativeText("More info")
        
        msg.setWindowTitle("nfo")
        
        msg.setDetailedText("The robot can be controlled by moving the system using arrow keys.\
            For this the Move Own check box on the gui should be turned off.\
            Make sure to press the keys intermittently. This is to enable constant movement without keyboard.\
            The sensor and the robot configuration can be changed via the configure buttons. The sensors available \
            for visualisation can be accessed via the visualise button. Only one parameter can be visualised per time.")
        
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        msg.exec_()

    def plot_data(self, d):
        """
        depending on how to plot
        plot only one value that is true
        """

        if self._plot_defualt_idx is not None:

            for idx, key in enumerate(self._plot_status[self._plot_defualt_idx]):

                if self._plot_status[self._plot_defualt_idx][key]:

                    self._canvas.add_data(d[idx])

                    break

    def drop_down(self, form):
        """
        create a interactive drop down menu
        the input param is form which is of two types
        either edit type or check type
        """

        self._sensor_list = QComboBox(self)

        for idx, sensor in enumerate(self._sensor_configs):

            if form == 'edit':
                
                self._sensor_list.addItem(sensor['name'])
                
                self._sensor_list.activated[str].connect(partial(self.pop_edit_up, idx))
                
                self._sensor_list.move(580, 150)
            
            elif form == 'check':
                
                if self.config_at_idx(idx)['plotable_vals'] is not None:
                    
                    self._sensor_list.addItem(sensor['name'])
                    
                    self._sensor_list.activated[str].connect(partial(self.pop_check_up, idx))
                    
                    self._sensor_list.move(580, 350)

        self._sensor_list.show()

    def pop_edit_up(self, sensor_idx):
        """
        The call back function to setup a edit type
        pop up. The input params are:
        Param: Sensor_idx :  integer denoting the index of the sensor
        """

        self._sensor_config = ConfigurePopup(self, 'edit', sensor_idx)
        
        self._sensor_config.move(self._width/2, self._height/2)

        self._sensor_config.show()

        if sensor_idx is not None:

            self._sensor_list.close()

    def pop_check_up(self, sensor_idx):
        """
        The call back function to setup a check type
        pop up. The input params are:
        Param: Sensor_idx :  integer denoting the index of the sensor
        """

        self._sensor_config = ConfigurePopup(self, 'check', sensor_idx)

        self._sensor_config.move(self._width/2, self._height/2)

        self._sensor_config.show()

        self._sensor_list.close()


    def robot_config(self):
        """
        Return the robot config file to the gui
        this is used for updation
        """

        return self._robot_config

    def config_at_idx(self, idx):
        """
        Return the sensor config to the gui
        if there are muliple sensors, the option
        is to the send the config at a particular index
        Params: idx: integer denoting the index of the sensor
        """

        return self._sensor_configs[idx]

    def update_configs(self, vals, idx):
        """
        This is the funciton that can be accessed
        via the gui to update the config parameters.
        Once called the corresponding sensor config dictionary
        is update using the vals provided.
        Params: vals : list of values having size equal to the dictionary params
                idx: integer denoting the index of the sensor
        """

        if idx is None:
            
            self._robot_config['params'].update({k : vals[i] for i,k in enumerate(self._robot_config['params'].keys())})
            
            self._rover_world.update_robot_config(self._robot_config)
        
        else:
            
            self._sensor_configs[idx]['params'].update({k : vals[i] for i,k in enumerate(self._sensor_configs[idx]['params'].keys())})
            
            self._rover_world.update_sensor_config(self._sensor_configs[idx], idx)


    def update_plots(self, vals, idx):
        """
        The function used to update the plots.
        Depending on which index of the sensor parameter is
        selected. Only one of the parameter can be plotted at a time.
        Params: vals: list of values having size equal to the plotable values
                idx: sensor index which has a plotable parameter
        """
        
        self._plot_status[idx] = vals

        self._plot_defualt_idx = idx

    def update_log_status(self, state):
        """
        Callback function from the check box in the panel.
        The input is the state of the q box. Based on the status
        the log will be either shown or turned off.
        """

        if state == Qt.Checked:

            self._rover_world.show_log(True)

        else:

            self._rover_world.show_log(False)


    def update_move_status(self, state):
        """
        Callback function from the check box in the panel.
        The input is the state of the q box. Based on the status
        the log will be either shown or turned off.
        """

        if state == Qt.Checked:

            self._rover_world.move_own(True)

        else:

            self._rover_world.move_own(False)


     
    def init_pygame(self, rover_world):
        """
        Initiate the pygame window loop
        Params: rover world of type tmr_world.world object
        """
        
        self._rover_world = rover_world

        self._timer = QTimer()

        self._timer.timeout.connect(self.pygame_loop)

        self._timer.start(0)

    def pygame_loop(self):
        """
        The pygmae loop to be run with the 
        qt window
        """

        if self._rover_world.run(self, self.plot_data):

            self.close()
