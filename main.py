import sys
import os
import gmm
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# import the converted file as ui
from qt5 import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.select_path.clicked.connect(self.open)
        self.ui.select_report_path.clicked.connect(self.report)
        self.ui.select_out_path.clicked.connect(self.output)
        self.ui.select_summary_path.clicked.connect(self.outputSummary)
        self.ui.select_cell_list_path.clicked.connect(self.outputCellList)
        # self.ui.actionAdd_file_from_directory.triggered.connect(self.open)
        # self.ui.actionAdd_file_from_csv.triggered.connect(self.ui.csv.click)
        # self.ui.actionAdd_file_from_csv.triggered.connect(self.open)
        self.ui.raw_data_path.currentIndexChanged.connect(self.grayhto)        
        # self.ui.output_path.setPlaceholderText("SSD_mtx/")
        self.ui.run.clicked.connect(self.parseCommand)
        self.ui.exit.clicked.connect(self.close)
        self.ui.actionExit.triggered.connect(self.close)
        # self.ui.textBox1.setText("==GMM-Demux Initialization==\n")
        self.setFocus()
        self.show()

    def open(self):
        if ((self.ui.raw_data_path.currentText() == "mtx file directory")
            | (self.ui.raw_data_path.currentText() == "full report directory")):
            directory_path = QFileDialog.getExistingDirectory(self, "Open a directory")
            if (directory_path != ('')):
                self.ui.path.setPlainText(directory_path)
        elif (self.ui.raw_data_path.currentText() == "csv file"):
            csv_path = QFileDialog.getOpenFileName(self, "Open a csv file", "", "*.csv")
            if (csv_path != ('','')):
                self.ui.path.setPlainText(csv_path[0])

    def grayhto(self):
        if (self.ui.raw_data_path.currentText() == "full report directory"):
            self.ui.hto_array.setStyleSheet("color: rgb(126, 126, 126); background-color: rgb(211, 211, 211);")
            self.ui.hto_array.setReadOnly(True)
        else:
            self.ui.hto_array.setStyleSheet("color: rgb(0, 0, 0); background-color: rgb(255, 255, 255);")
            self.ui.hto_array.setReadOnly(False)

    def output(self):
        output_path = QFileDialog.getExistingDirectory(self, "Open a directory")
        if (output_path != ('','')):
            self.ui.output_path.setPlainText(output_path)

    def report(self):
        report_path = QFileDialog.getExistingDirectory(self, "Open a directory")
        if (report_path != ('')):
            self.ui.report_path.setPlainText(report_path)

    def outputSummary(self):
        summary_path = QFileDialog.getOpenFileName(self, "Open a file", "", "All Files (*.*)")
        if (summary_path != ('','')):
            self.ui.summary_path.setPlainText(summary_path[0])

    def outputCellList(self):
        cell_list_path = QFileDialog.getOpenFileName(self, "Open a file", "", "All Files (*.*)")
        if (cell_list_path != ('','')):
            self.ui.cell_list_path.setPlainText(cell_list_path[0])

    def parseCommand(self):
        command = "GMM-demux"
        if (self.ui.raw_data_path.currentText() == "full report directory"):
            command = command + " -k " + self.ui.path.toPlainText()
        else:
            command = command + " " + self.ui.path.toPlainText() + " " + self.ui.hto_array.toPlainText()
            if (self.ui.raw_data_path.currentText() == "csv file"):
                command = command + " -c"
        if (self.ui.output_path.toPlainText()):
            command = command + " -o " + self.ui.output_path.toPlainText()
        if (self.ui.hto_tags.toPlainText()):
            command = command + " -x " + self.ui.hto_tags.toPlainText()
        if (self.ui.report_path.toPlainText()):
            if (self.ui.report_type.currentText() == "full"):
                command = command + " -f "
            elif (self.ui.report_type.currentText() == "simplified"):
                command = command + " -s "
            command = command + self.ui.report_path.toPlainText()
        if (self.ui.summary_path.toPlainText()):
            command = command + " -r " + self.ui.summary_path.toPlainText()
        if (self.ui.cell_list_path.toPlainText()):
            command = command + " -e " + self.ui.cell_list_path.toPlainText()
        if (self.ui.threshold.toPlainText()):
            command = command + " -t " + self.ui.threshold.toPlainText()
        if (self.ui.cell_count.toPlainText()):
            command = command + " -u " + self.ui.cell_count.toPlainText()
        if (self.ui.phony_chance.toPlainText()):
            command = command + " -a " + self.ui.phony_chance.toPlainText()
        

        print(command)
        # gmm.main(command)

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())