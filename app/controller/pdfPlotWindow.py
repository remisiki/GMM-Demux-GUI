from controller.init.pdfPlotWindow import Ui_PdfPlotDialog
from PyQt5.QtWidgets import QDialog

class pdfPlotWindow(QDialog):
    def __init__(self, parent=None, hto_array=None):
        super(pdfPlotWindow, self).__init__(parent)
        self.ui = Ui_PdfPlotDialog()
        self.ui.setupUi(self)
        self.ui.hto_to_plot.addItems(hto_array)