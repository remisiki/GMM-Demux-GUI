from app.controller.init.classifierWindow import Ui_ClassifierDialog
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QListWidgetItem
from functools import reduce

class ClassifierWindow(QDialog):
    def __init__(self, parent=None):
        super(ClassifierWindow, self).__init__(parent)
        self.ui = Ui_ClassifierDialog()
        self.ui.setupUi(self)
        self.ui.threshold.textChanged.connect(self.thresholdCheck)
        self.threshold_correct_style = self.ui.threshold.styleSheet()
        self.ui.threshold_err_label.hide()

    def setList(self, list):
        for name in list:
            item = QListWidgetItem(name)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.ui.hto_tags_selection.addItem(item)

    def addHto(self):
        extract_ary = []
        for index in range(self.ui.hto_tags_selection.count()):
            item = self.ui.hto_tags_selection.item(index)
            if (item.checkState() == QtCore.Qt.Checked):
                extract_ary.append(item.text())
        if (extract_ary):
            extract_ary_str = reduce((lambda a, b: f"{a}+{b}"), extract_ary)
            item = QListWidgetItem(extract_ary_str)
            self.ui.hto_tags.addItem(item)

    def removeHto(self):
        pos = self.ui.hto_tags.currentRow()
        dump = self.ui.hto_tags.takeItem(pos)
        del dump

    def thresholdCheck(self):
        threshold = self.ui.threshold.toPlainText()
        try:
            threshold = float(threshold)
        except:
            self.thresholdError()
            return

        if (threshold > 1 or threshold < 0):
            self.thresholdError()
            return

        self.thresholdCorrect()

    def thresholdError(self):
        self.ui.threshold.setStyleSheet("border-color: red;")
        self.ui.threshold_err_label.show()
        self.ui.OK.setEnabled(False)

    def thresholdCorrect(self):
        self.ui.threshold.setStyleSheet(self.threshold_correct_style)
        self.ui.threshold_err_label.hide()
        self.ui.OK.setEnabled(True)
