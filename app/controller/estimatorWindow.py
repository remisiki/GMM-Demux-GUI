from controller.init.estimatorWindow import Ui_EstimatorDialog
from PyQt5.QtWidgets import QDialog, QFileDialog

class EstimatorWindow(QDialog):
    def __init__(self, parent=None):
        super(EstimatorWindow, self).__init__(parent)
        self.ui = Ui_EstimatorDialog()
        self.ui.setupUi(self)
        self.ui.open_examine_path.clicked.connect(self.setExamineCellPath)
        self.ui.ambiguous_rate.textChanged.connect(self.ambiguousCheck)
        self.ambiguousCorrectStyle = self.ui.ambiguous_rate.styleSheet()
        self.ui.ambiguous_rate_err_label.hide()

    def setExamineCellPath(self):
        input_path = QFileDialog.getOpenFileName(self, "Open a text file", "", "*.txt")
        if (input_path == ('','')):
            return
        self.ui.examine_cell_path.setPlainText(input_path[0])

    def ambiguousCheck(self):
        ambiguous_rate = self.ui.ambiguous_rate.toPlainText()
        try:
            ambiguous_rate = float(ambiguous_rate)
        except:
            self.ambiguousError()
            return

        if (ambiguous_rate > 1 or ambiguous_rate < 0):
            self.ambiguousError()
            return

        self.ambiguousCorrect()

    def ambiguousError(self):
        self.ui.ambiguous_rate.setStyleSheet("border-color: red;")
        self.ui.ambiguous_rate_err_label.show()
        self.ui.OK.setEnabled(False)

    def ambiguousCorrect(self):
        self.ui.ambiguous_rate.setStyleSheet(self.ambiguousCorrectStyle)
        self.ui.ambiguous_rate_err_label.hide()
        self.ui.OK.setEnabled(True)
