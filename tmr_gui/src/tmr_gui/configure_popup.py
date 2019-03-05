#!/usr/bin/env python3
"""Provides GUI which creates the control panel pop up for the tmr robot.
The class provides a fully extendable ways to add popups at present
with editable types and checkboxed with respect to the config file.

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

from PyQt5.QtCore import Qt
from functools import partial
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QFont, QPainter
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QFormLayout, QCheckBox


class ConfigurePopup(QWidget):

    def __init__(self, parent, form='edit', idx=None):
        """
        Constructor of the class
        params: parent = type tmr_gui.gui
        form : 'edit' or 'check' to denote the type of popup
        idx : integer number denoting sensor index, robot index 
        """


        QWidget.__init__(self)

        self._parent = parent

        if form =='edit' and idx is not None:

            self.init_edit_layout(idx)

        elif form=='check' and idx is not None:

            self.init_check_layout(idx)


    def init_edit_layout(self, idx):
        """
        Create the edit layout
        Params: idx: integer number denoting sensor index, robot index 
        """


        if idx is None:

            self._config_vals = self._parent.robot_config()
        
        else:
            
            self._config_vals = self._parent.config_at_idx(idx)
        
        self.init_edit_lines()

        self._idx = idx


    def init_check_layout(self, idx):
        """ 
        Create the check layout
        Params: idx: integer number denoting sensor index, robot index 
        """
  
        self._config_vals = self._parent.config_at_idx(idx)
        
        self.init_check_lines()


    def init_check_lines(self):
        """
        Call back funciton to create the check type box
        """

        self._config_check_lines = []

        layout = QFormLayout()

        self._chk_vals = None

        if self._config_vals['plotable_vals'] is not None:

            self._chk_vals = []

            for idx, key in enumerate(self._config_vals['plotable_vals']):

                self._config_check_lines.append(QCheckBox())

                if idx == 0:

                    self._config_check_lines[-1].setChecked(True)

                    self._chk_vals.append(True)

                else:

                    self._chk_vals.append(False)

                self._config_check_lines[-1].stateChanged.connect(partial(self.update_chk_callback, idx))

                layout.addRow(key, self._config_check_lines[-1])

            self.setLayout(layout)

            self.setWindowTitle("Visualize " + self._config_vals['name'] + "Values")
        
    
    def init_edit_lines(self):
        """
        Call back function to create edit type box
        """

        self._config_edit_lines = []

        layout = QFormLayout()

        for idx, key in enumerate(self._config_vals['params']):

            self._config_edit_lines.append(QLineEdit())

            self._config_edit_lines[-1].setValidator(QDoubleValidator())
        
            self._config_edit_lines[-1].setText(str(self._config_vals['params'][key]))

            layout.addRow(key, self._config_edit_lines[-1])

        self._update_bt = QPushButton("Update", self)

        layout.addRow(self._update_bt)

        self._update_bt.clicked.connect(self.update_bt_callback)

        self.setLayout(layout)

        self.setWindowTitle("Modify " + self._config_vals['name'] + " Config")


    def update_bt_callback(self):
        """
        The update button callback
        this fuction reads the new parameters of the 
        pop up window and sends it to the parent gui to 
        be updated
        """
        
        vals = []

        for key_line in self._config_edit_lines:

            vals.append( float(key_line.text()) )

        self._parent.update_configs(vals, self._idx)

        self.close()


    def update_chk_callback(self, idx, state):
        """
        The update check button callback
        this fuction reads the new parameters of the 
        pop up window and sends it to the parent gui to 
        be updated
        """

        if self._chk_vals is not None:

            if state == Qt.Checked:

                self._chk_vals[idx] = True

                for k in range(len(self._config_check_lines)):

                    if k == idx:

                        continue

                    self._config_check_lines[k].setChecked(False)
            
            else:
                
                self._chk_vals[idx] = False

            self._parent.update_plots(self._chk_vals, self._idx)

    def config_vals(self):
        """
        Return the config values
        """

        return self._config_vals

