import sys
import os
import gmm
from gmmd import compute, estimator, classifier, io, plot
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QFileDialog, QTextEdit, QTextBrowser, QDialogButtonBox, QVBoxLayout, QLabel, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QFile, QTextStream, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
from qt5 import Ui_MainWindow
from classifierWindow import Ui_ClassifierWindow
from breeze import breeze_resources
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import time
import threading
import tempfile

class Worker(QObject):
    finished = pyqtSignal()
    response = pyqtSignal(object)

    def __init__(self, f, args = None, parent = None):
        QThread.__init__(self, parent)
        self.f = f
        self.args = args

    def func(self):
        if (self.args):
            result = self.f(*self.args)
        else:
            result = self.f()
        self.finished.emit()
        self.response.emit(result)

class ClassifierWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ClassifierWindow, self).__init__(parent)
        self.ui = Ui_ClassifierWindow()
        self.ui.setupUi(self)

class MainWindow(QMainWindow):
    tmp_path = os.path.join(tempfile.gettempdir(), ".gmm-demux")
    full_df = None
    GMM_df = None
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
        self.ui.actionQuick_Read.triggered.connect(self.readData)
        self.ui.actionRun.triggered.connect(self.parseCommand)
        self.ui.actionClassify.triggered.connect(self.runClassifier)
        self.ui.actionPlot.triggered.connect(self.plot)
        self.ui.actionSave_MSM_free_results_to.triggered.connect(lambda: self.saveResult(ssd = True))
        self.ui.actionSave_full_results_to.triggered.connect(lambda: self.saveResult(full = True))
        self.ui.actionSave_simplified_results_to.triggered.connect(lambda: self.saveResult(full = False))
        self.ui.raw_data_path.currentIndexChanged.connect(self.grayhto)
        self.ui.read.clicked.connect(self.readData)
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

    def asyncFunc(self, func, args = None, after = None):
        self.thread = QThread(self)
        self.worker = Worker(f = func, args = args)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.func)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        if (after):
            self.thread.finished.connect(after)

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

    def readData(self):
        def readDataHelper(input_mode, input_path, hto_array = None):
            if (input_mode == "mtx file directory"):
                self.full_df, self.GMM_df = io.read_cellranger(input_path, hto_array)
            elif (input_mode == "csv file"):
                self.full_df, self.GMM_df = io.read_csv(input_path, hto_array)
            self.GEM_num = self.GMM_df.shape[0]
            self.sample_num = self.GMM_df.shape[1]
            self.base_bv_array = compute.obtain_base_bv_array(self.sample_num)

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Loading")
        dlg.setStandardButtons(QMessageBox.NoButton)
        dlg.setText("Reading cell data...")
        dlg.show()
        input_mode = self.ui.raw_data_path.currentText()
        input_path = self.ui.path.toPlainText()
        hto_array = self.ui.hto_array.toPlainText().split(',')
        self.asyncFunc(
            func = readDataHelper, 
            args = [
                input_mode,
                input_path, 
                hto_array
            ],
            after = lambda: (
                    dlg.setText("Done."),
                    dlg.setStandardButtons(QMessageBox.Ok)
                )
        )

    def saveResult(self, full = True, ssd = False):
        def ssdSaveHelper(output_path):
            self.purified_df = classifier.purify_droplets(self.GMM_full_df, self.confidence_threshold)
            SSD_idx = classifier.obtain_SSD_list(self.purified_df, self.sample_num, self.extract_id_ary)
            io.store_cellranger(self.full_df, SSD_idx, output_path)

        output_path = QFileDialog.getExistingDirectory(self, "Open a directory")
        if (output_path == ('','')):
            return
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Loading")
        dlg.setStandardButtons(QMessageBox.NoButton)
        dlg.setText("Saving...")
        dlg.show()
        if (ssd):
            self.asyncFunc(
                func = ssdSaveHelper,
                args = [
                    output_path
                ],
                after = lambda: (
                        dlg.setText("Done."),
                        dlg.setStandardButtons(QMessageBox.Ok)
                    )
            )
        elif (full):
            self.asyncFunc(
                func = classifier.store_full_classify_result,
                args = [
                    self.GMM_full_df,
                    self.class_name_ary,
                    output_path
                ],
                after = lambda: (
                        dlg.setText("Done."),
                        dlg.setStandardButtons(QMessageBox.Ok)
                    )
            )
        else:
            self.asyncFunc(
                func = classifier.store_simplified_classify_result,
                args = [
                    self.GMM_full_df,
                    self.class_name_ary,
                    output_path,
                    self.sample_num,
                    self.confidence_threshold
                ],
                after = lambda: (
                        dlg.setText("Done."),
                        dlg.setStandardButtons(QMessageBox.Ok)
                    )
            )

    def parseCommand(self):
        print(self.GMM_full_df)
        print(self.class_name_ary)
        return
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
        self.plot()
        self.ui.console.append("Finished in {0: .2f}s.\n".format(time.time() - start_time))

    def plot(self):
        def plotHelper():
            # plot.tsne_plot(self.GMM_df, self.GMM_full_df)
            pass
        # df = pd.read_csv(self.ui.plot_path.toPlainText())
        # if (self.ui.plot_type.currentText() == "scatter"):
        #     x = df.iloc[:, 0].values
        #     y = df.iloc[:, 1].values
        #     plt.scatter(x, y)
        #     # print("sct")
        #     self.ui.console.append("Scatter plot generated.\n")
        # elif (self.ui.plot_type.currentText() == "distribution"):
        #     sns.displot(df)
        #     # print("dist")
        #     self.ui.console.append("Distribution plot generated.\n")
        # plt.savefig(self.tmp_path + "plot.png")
        if (self.ui.plot_type.currentText() == "distribution"):
            hto_name = self.ui.plot_path.toPlainText()
            pixmap = QPixmap(self.tmp_path + f"pdf_{hto_name}.png")
        elif (self.ui.plot_type.currentText() == "tSNE"):
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Loading")
            dlg.setStandardButtons(QMessageBox.NoButton)
            dlg.setText("Plotting tSNE, it may take a few minutes...")
            dlg.show()
            self.asyncFunc(
                func = plotHelper,
                after = lambda: (
                    self.ui.label_plot.setPixmap(
                        QPixmap(os.path.join(self.tmp_path, "tsne.png")).scaled(self.ui.label_plot.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    ),
                    dlg.setText("Done."),
                    dlg.setStandardButtons(QMessageBox.Ok)
                )
            )

        # pixmap = pixmap.scaled(self.ui.label_plot.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # self.ui.label_plot.setPixmap(pixmap)

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

    def setThreshold(self):
        self.confidence_threshold = float(self.classifierWindow.ui.threshold.toPlainText())

    def setExtract(self):
        self.extract_id_ary = self.classifierWindow.ui.hto_tags.toPlainText()
        if (not self.extract_id_ary):
            return
        extract_id_ary = []
        tag_name_ary = []
        hto_array = self.ui.hto_array.toPlainText().split(',')

        for tag_name in self.extract_id_ary.split(','):
            tag_name_ary.append(tag_name.split('+') )

        for tag_ary in tag_name_ary:
            mask = compute.init_mask(self.sample_num)
            for tag in tag_ary:
                hto_idx = hto_array.index(tag)
                bv = compute.set_bit(mask, hto_idx)

            for idx in range(0, len(self.base_bv_array) ):
                if self.base_bv_array[idx] == mask:
                    extract_id = idx

            extract_id_ary.append(extract_id)
        self.extract_id_ary = extract_id_ary

    def runClassifier(self):
        def runClassifierHelper():
            high_array, low_array = classifier.obtain_arrays(self.GMM_df)
            self.GMM_full_df, self.class_name_ary = classifier.classify_drops(self.base_bv_array, high_array, low_array, self.GMM_df)
        def runClassifierWorker():
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Loading")
            dlg.setStandardButtons(QMessageBox.NoButton)
            dlg.setText("Running classifier...")
            dlg.show()
            self.asyncFunc(
                func = runClassifierHelper, 
                after = lambda: (
                        dlg.setText("Done."),
                        dlg.setStandardButtons(QMessageBox.Ok)
                    )
            )

        self.classifierWindow = ClassifierWindow(self)
        self.classifierWindow.show()
        self.classifierWindow.ui.OK.clicked.connect(
            lambda: (
                self.setThreshold(),
                self.setExtract(),
                self.classifierWindow.close(),
                runClassifierWorker()
            )
        )
        return

        

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