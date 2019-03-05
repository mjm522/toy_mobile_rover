#!/usr/bin/env python3
"""Provides GUI which creates the plot panel pop up for the tmr robot.

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

import sys
import matplotlib
import numpy as np
matplotlib.use("Qt4Agg")
from collections import deque
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
from PyQt5.QtCore import QObject, pyqtSignal
from matplotlib.animation import TimedAnimation
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


class EmbedPlot(FigureCanvas, TimedAnimation):

    def __init__(self, maxlen=20):
        """
        Class contstructor
        Param: maxlen: number of values in the plot
        window. This helps to avoid resizing of the window
        """

        self._data = deque(maxlen=maxlen)

        # The data
        self._xlim = 200

        self._n = np.linspace(0, self._xlim - 1, self._xlim)
        
        self._y = (self._n * 0.0)

        # The window
        self._fig = Figure(figsize=(5,5), dpi=100)
        
        self._ax1 = self._fig.add_subplot(111)

        # self._ax1 settings
        self._ax1.set_xlabel('time')
        
        self._ax1.set_ylabel('raw data')
        
        self._line1 = Line2D([], [], color='blue')
        
        self._line1_tail = Line2D([], [], color='red', linewidth=2)
        
        self._line1_head = Line2D([], [], color='red', marker='o', markeredgecolor='r')
        
        self._ax1.add_line(self._line1)
        
        self._ax1.add_line(self._line1_tail)
        
        self._ax1.add_line(self._line1_head)
        
        self._ax1.set_xlim(0, self._xlim - 1)
        
        self._ax1.set_ylim(0, 100)

        FigureCanvas.__init__(self, self._fig)

        TimedAnimation.__init__(self, self._fig, interval = 50, blit = True)


    # def data_receiver(self, add_data_callback):

    #     self._src = Communicate()
        
    #     self._src.data_signal.connect(add_data_callback)


    def new_frame_seq(self):
        """
        Create new frame sequence
        """

        return iter(range(self._n.size))

    def _init_draw(self):
        """
        Set the axis lines
        """

        lines = [self._line1, self._line1_tail, self._line1_head]
        
        for l in lines:
            
            l.set_data([], [])

    def add_data(self, value):
        """
        Add data to the data list
        """

        self._data.append(value)

    def _step(self, *args):
        """
        Step through the animation
        or plot
        """
       
        try:

            TimedAnimation._step(self, *args)

        except Exception as e:

            TimedAnimation._stop(self)

            pass

    def _draw_frame(self, framedata):
        """
        Draw the frame of the robot
        """
        
        margin = 2
        
        while(len(self._data) > 0):
            
            self._y = np.roll(self._y, -1)
            
            self._y[-1] = self._data[0]
            
            del(self._data[0])


        self._line1.set_data(self._n[ 0 : self._n.size - margin ], self._y[ 0 : self._n.size - margin ])
        
        self._line1_tail.set_data(np.append(self._n[-10:-1 - margin], self._n[-1 - margin]), np.append(self._y[-10:-1 - margin], self._y[-1 - margin]))
        
        self._line1_head.set_data(self._n[-1 - margin], self._y[-1 - margin])
        
        self._drawn_artists = [self._line1, self._line1_tail, self._line1_head]


class Communicate(QObject):
    """
    This class is for creating
    a real time streaming class of data
    to the plot window. 
    """

    data_signal = pyqtSignal(float)