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

        return iter(range(self._n.size))

    def _init_draw(self):

        lines = [self._line1, self._line1_tail, self._line1_head]
        
        for l in lines:
            
            l.set_data([], [])

    def add_data(self, value):

        self._data.append(value)

    # def zoomIn(self, value):

    #     bottom = self._ax1.get_ylim()[0]

    #     top = self._ax1.get_ylim()[1]
        
    #     bottom += value
        
    #     top -= value
        
    #     self._ax1.set_ylim(bottom,top)
        
    #     self.draw()


    def _step(self, *args):
        # Extends the _step() method for the TimedAnimation class.
        try:
            TimedAnimation._step(self, *args)
        except Exception as e:
            # self.abc += 1
            # print(str(self.abc))
            TimedAnimation._stop(self)
            pass

    def _draw_frame(self, framedata):
        
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

    data_signal = pyqtSignal(float)