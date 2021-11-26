import sys
import os
import gmm
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QFileDialog, QTextEdit, QTextBrowser, QDialogButtonBox, QVBoxLayout, QLabel, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QFile, QTextStream
from PyQt5.QtGui import QPixmap
from qt5 import Ui_MainWindow
from breeze import breeze_resources
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import time

# class Ui_error(object):
#     def setupUi(self, error):
#         error.setObjectName("error")
#         error.resize(400, 300)
#         icon = QtGui.QIcon.fromTheme("no")
#         error.setWindowIcon(icon)
#         self.buttonBox = QtWidgets.QDialogButtonBox(error)
#         self.buttonBox.setGeometry(QtCore.QRect(180, 230, 171, 32))
#         self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
#         self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
#         self.buttonBox.setObjectName("buttonBox")

#         self.retranslateUi(error)
#         self.buttonBox.accepted.connect(error.accept)
#         self.buttonBox.rejected.connect(error.reject)
#         QtCore.QMetaObject.connectSlotsByName(error)

#     def retranslateUi(self, error):
#         _translate = QtCore.QCoreApplication.translate
#         error.setWindowTitle(_translate("error", "Error"))

class ErrorWindow(QDialog):
    def __init__(self, parent=None):
        # super(self).__init__(parent)
        # self.ui = Ui_error()
        # self.ui.setupUi(self)
        # self.show()
        super().__init__(parent)
        self.setWindowTitle("Error")
        QBtn = QDialogButtonBox.Ok# | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        # self.buttonBox.rejected.connect(self.reject)
        self.layout = QVBoxLayout()
        message = QLabel("Please plot your data first.")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class MainWindow(QMainWindow):
    tmp_path = "/tmp/.gmm-demux/"
    def __init__(self, parent=None):
        if (not os.path.exists(self.tmp_path)):
            os.makedirs(self.tmp_path)
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.console.append(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S ") + "GMM-demux started.\n")
        self.ui.select_path.clicked.connect(self.open)
        self.ui.select_report_path.clicked.connect(self.report)
        self.ui.select_out_path.clicked.connect(self.output)
        self.ui.select_summary_path.clicked.connect(self.outputSummary)
        self.ui.select_cell_list_path.clicked.connect(self.outputCellList)
        self.ui.select_plot_path.clicked.connect(self.inputPlot)
        self.ui.save_png.clicked.connect(self.savePlot)
        self.ui.actionAdd_file_from_directory.triggered.connect(lambda: self.ui.raw_data_path.setCurrentIndex(0))
        self.ui.actionAdd_file_from_directory.triggered.connect(self.open)
        self.ui.actionAdd_file_from_csv.triggered.connect(lambda: self.ui.raw_data_path.setCurrentIndex(1))
        self.ui.actionAdd_file_from_csv.triggered.connect(self.open)
        self.ui.actionAdd_full_report.triggered.connect(lambda: self.ui.raw_data_path.setCurrentIndex(2))
        self.ui.actionAdd_full_report.triggered.connect(self.open)
        self.ui.raw_data_path.currentIndexChanged.connect(self.grayhto)
        self.ui.run.clicked.connect(self.parseCommand)
        self.ui.plot.clicked.connect(self.plot)
        self.ui.exit.clicked.connect(self.close)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.gridLayout.addWidget(self.ui.frame_control, 0, 0, 2, 3)
        self.ui.gridLayout.addWidget(self.ui.frame_plot, 0, 3, 2, 2)
        self.ui.gridLayout.addWidget(self.ui.tabWidget_console, 2, 0, 2, 4)
        self.ui.gridLayout.addWidget(self.ui.frame_buttons, 2, 4, 2, 1)
        self.ui.actionLight.triggered.connect(lambda: changeTheme("light"))
        self.ui.actionDark.triggered.connect(lambda: changeTheme("dark"))
        self.ui.statusbar.showMessage("Ready")
        self.setFocus()
        self.show()
        # print(self.ui.frame_plot.size())

    def open(self):
        file_type = self.ui.raw_data_path.currentText()
        if ((file_type == "mtx file directory")
            | (file_type == "full report directory")):
            directory_path = QFileDialog.getExistingDirectory(self, "Open a directory")
            if (directory_path != ('')):
                self.ui.path.setPlainText(directory_path)
        elif (file_type == "csv file"):
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
        start_time = time.time()
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
        

        # sys.stdout.write(command)
        # print(self.size())
        string = gmm.main(command)
        # print(string)
        self.ui.console.append(string)
        self.ui.console.append("Finished in {0: .2f}s.\n".format(time.time() - start_time))

    def plot(self):
        df = pd.read_csv(self.ui.plot_path.toPlainText())
        if (self.ui.plot_type.currentText() == "scatter"):
            x = df.iloc[:, 0].values
            y = df.iloc[:, 1].values
            plt.scatter(x, y)
            # print("sct")
            self.ui.console.append("Scatter plot generated.\n")
        elif (self.ui.plot_type.currentText() == "distribution"):
            sns.displot(df)
            # print("dist")
            self.ui.console.append("Distribution plot generated.\n")
        plt.savefig(self.tmp_path + "plot.png")
        pixmap = QPixmap(self.tmp_path + "plot.png")
        pixmap = pixmap.scaled(self.ui.label_plot.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ui.label_plot.setPixmap(pixmap)

    def inputPlot(self):
        csv_path = QFileDialog.getOpenFileName(self, "Open a csv file", "", "*.csv")
        if (csv_path != ('','')):
            self.ui.plot_path.setPlainText(csv_path[0])

    def resizeEvent(self, event):
        self.plotResize()
        # print(self.ui.label_plot.size())
        return super(QMainWindow, self).resizeEvent(event)

    def closeEvent(self, event):
        if (os.path.exists(self.tmp_path + "plot.png")):
            os.remove(self.tmp_path + "plot.png")
        event.accept() # let the window close

    def plotResize(self):
        if (os.path.exists(self.tmp_path + "plot.png")):
            pixmap = QPixmap(self.tmp_path + "plot.png")
            pixmap = pixmap.scaled(self.ui.label_plot.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.ui.label_plot.setPixmap(pixmap)

    def savePlot(self):
        if (not os.path.exists(self.tmp_path + "plot.png")):
            # dlg = ErrorWindow(self)
            # if (dlg.exec()):
            #     print("ss")
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("Please plot your data first")
            dlg.exec()
            return
        path = QFileDialog.getSaveFileName(self, "Save file", "", "*.png")
        if (path != ('','')):

            os.system("cp " + self.tmp_path + "plot.png " + path[0])
            self.ui.console.append("Saved plot image as " + path[0] + '\n')

def changeTheme(theme_type):
    file = QFile("./breeze/dist/" + theme_type + "/stylesheet.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    QApplication.instance().setStyleSheet(stream.readAll())


def main():
    app = QApplication(sys.argv)
    # app.setStyle('Windows')
    # app.setStyleSheet(qdarkstyle.load_stylesheet())
    # print(QtWidgets.QStyleFactory.keys())
    file = QFile("./breeze/dist/dark/stylesheet.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())
    width = app.primaryScreen().size().width()
    # print(width)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()