from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QFont, QPainter
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QFormLayout


class ConfigurePopup(QWidget):

    def __init__(self, parent, idx):

        QWidget.__init__(self)

        self._parent = parent

        if idx is None:
            self._config_vals = self._parent.robot_config()
        else:
            self._config_vals = self._parent.config_at_idx(idx)
        
        self._idx = idx
        
        self.init_key_lines()
        
    def init_key_lines(self):

        self._config_key_lines = []

        self._layout = QFormLayout()

        for idx, key in enumerate(self._config_vals['params']):

            self._config_key_lines.append(QLineEdit())

            self._config_key_lines[-1].setValidator(QDoubleValidator())
        
            self._config_key_lines[-1].setText(str(self._config_vals['params'][key]))

            self._layout.addRow(key, self._config_key_lines[-1])

        self._update_bt = QPushButton("Update", self)

        self._layout.addRow(self._update_bt)

        self._update_bt.clicked.connect(self.update_callback)

        self.setLayout(self._layout)

        self.setWindowTitle("Modify " + self._config_vals['name'] + " Config")


    def update_callback(self):
        
        vals = []

        for key_line in self._config_key_lines:

            vals.append( float(key_line.text()) )

        self._parent.update_configs(vals, self._idx)

        self.close()

    def config_vals(self):

        return self._config_vals