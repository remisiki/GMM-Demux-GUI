from controller.init.htoWindow import Ui_HtoDialog
from PyQt5.QtWidgets import QDialog

class HtoWindow(QDialog):
    def __init__(self, parent=None):
        super(HtoWindow, self).__init__(parent)
        self.ui = Ui_HtoDialog()
        self.ui.setupUi(self)