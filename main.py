import sys
import os
import gmm
from gmmd import compute, estimator, classifier, io, plot
import datetime
import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QFileDialog, QTextEdit, QTextBrowser, QDialogButtonBox, QVBoxLayout, QLabel, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QFile, QTextStream, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMenu, QAction
from qt5 import Ui_MainWindow
from classifierWindow import Ui_ClassifierDialog
from estimatorWindow import Ui_EstimatorDialog
from htoWindow import Ui_HtoDialog
from pdfPlotWindow import Ui_PdfPlotDialog
from breeze import breeze_resources
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import time
import threading
import tempfile
from pandasTable import *
import shutil

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

class ClassifierWindow(QDialog):
    def __init__(self, parent=None):
        super(ClassifierWindow, self).__init__(parent)
        self.ui = Ui_ClassifierDialog()
        self.ui.setupUi(self)

class EstimatorWindow(QDialog):
    def __init__(self, parent=None):
        super(EstimatorWindow, self).__init__(parent)
        self.ui = Ui_EstimatorDialog()
        self.ui.setupUi(self)

class HtoWindow(QDialog):
    def __init__(self, parent=None):
        super(HtoWindow, self).__init__(parent)
        self.ui = Ui_HtoDialog()
        self.ui.setupUi(self)

class pdfPlotWindow(QDialog):
    def __init__(self, parent=None, hto_array=None):
        super(pdfPlotWindow, self).__init__(parent)
        self.ui = Ui_PdfPlotDialog()
        self.ui.setupUi(self)
        self.ui.hto_to_plot.addItems(hto_array)

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
        self.ui.actionAdd_file_from_directory.triggered.connect(lambda: self.readData(input_mode = "mtx"))
        self.ui.actionAdd_file_from_csv.triggered.connect(lambda: self.readData(input_mode = "csv"))
        # self.ui.actionAdd_full_report.triggered.connect(lambda: self.ui.raw_data_path.setCurrentIndex(2))
        # self.ui.actionAdd_full_report.triggered.connect(self.open)
        self.ui.actionQuick_Read.triggered.connect(self.readData)
        self.ui.actionRun.triggered.connect(self.parseCommand)
        self.ui.actionClassify.triggered.connect(self.runClassifier)
        self.ui.actionPDF.triggered.connect(lambda: self.plot(plot_type = "pdf"))
        self.ui.actiontSNE.triggered.connect(lambda: self.plot(plot_type = "tsne"))
        self.ui.actionSave_MSM_free_results_to.triggered.connect(lambda: self.saveResult(ssd = True))
        self.ui.actionSave_full_results_to.triggered.connect(lambda: self.saveResult(full = True))
        self.ui.actionSave_simplified_results_to.triggered.connect(lambda: self.saveResult(full = False))
        self.ui.actionEstimate.triggered.connect(self.runEstimator)
        self.ui.read.clicked.connect(self.readData)
        self.ui.classify.clicked.connect(self.runClassifier)
        self.ui.estimate.clicked.connect(self.runEstimator)
        # self.ui.plot.clicked.connect(self.plot)
        self.ui.exit.clicked.connect(self.close)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.gridLayout.addWidget(self.ui.frame_control, 0, 0, 2, 3)
        self.ui.gridLayout.addWidget(self.ui.frame_plot, 0, 3, 2, 2)
        self.ui.gridLayout.addWidget(self.ui.tabWidget_console, 2, 0, 2, 4)
        self.ui.gridLayout.addWidget(self.ui.frame_buttons, 2, 4, 2, 1)
        self.ui.actionLight.triggered.connect(lambda: changeTheme("light"))
        self.ui.actionDark.triggered.connect(lambda: changeTheme("dark"))
        self.ui.statusbar.showMessage("Ready")
        self.ui.perSampleTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.perSampleTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.perSampleTable.setVerticalHeaderLabels(["Cell count", "SSD count", "Relative SSM rate"])
        # setattr(QLabel, 'plotMenu', self.plotMenu)
        self.ui.label_plot.customContextMenuRequested.connect(self.plotMenu)
        self.plot_file_name = None
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

    def outputSummary(self):
        summary_path = QFileDialog.getOpenFileName(self, "Open a file", "", "All Files (*.*)")
        if (summary_path != ('','')):
            self.ui.summary_path.setPlainText(summary_path[0])

    def outputCellList(self):
        cell_list_path = QFileDialog.getOpenFileName(self, "Open a file", "", "All Files (*.*)")
        if (cell_list_path != ('','')):
            self.ui.cell_list_path.setPlainText(cell_list_path[0])

    def openDialog(self, title = "Info", text = "", buttonStyle = QMessageBox.NoButton):
        dlg = QMessageBox(self)
        dlg.setWindowTitle(title)
        dlg.setStandardButtons(buttonStyle)
        dlg.setText(text)
        dlg.show()
        return dlg

    def setHtoArray(self):
        self.hto_array = self.htoWindow.ui.hto_array.toPlainText().split(',')

    def readData(self, input_mode = None):
        def readDataHelper(input_mode, input_path, hto_array = None):
            if (input_mode == "mtx" or (not input_mode)):
                self.full_df, self.GMM_df = io.read_cellranger(input_path, hto_array)
            elif (input_mode == "csv"):
                self.full_df, self.GMM_df = io.read_csv(input_path, hto_array)
            self.GEM_num = self.GMM_df.shape[0]
            self.sample_num = self.GMM_df.shape[1]
            self.base_bv_array = compute.obtain_base_bv_array(self.sample_num)

        def readDataWorker(input_mode, input_path):
            dlg = self.openDialog(text = "Reading data...")
            self.asyncFunc(
                func = readDataHelper, 
                args = [
                    input_mode,
                    input_path, 
                    self.hto_array
                ],
                after = lambda: (
                        self.ui.tabWidget_console.setCurrentIndex(1),
                        self.ui.GEM_num.setPlainText(str(self.GEM_num)),
                        self.ui.sample_num.setPlainText(str(self.sample_num)),
                        self.ui.dataTable.setTableWidget(self.full_df),
                        dlg.setText("Done."),
                        dlg.setStandardButtons(QMessageBox.Ok),
                        self.ui.actionClassify.setEnabled(True)
                    )
            )

        if (input_mode == "mtx"):
            input_path = QFileDialog.getExistingDirectory(self, "Open a directory")
            if (input_path == ('')):
                return
        elif (input_mode == "csv"):
            input_path = QFileDialog.getOpenFileName(self, "Open a csv file", "", "*.csv")
            if (input_path == ('','')):
                return
        elif (not input_mode):
            input_path = r"/run/media/setsunayyw/0D7D06240D7D0624/SJTU/2021-09/研究/GMM-Demux-GUI/example_input/outs/filtered_feature_bc_matrix"

        self.htoWindow = HtoWindow(self)
        self.htoWindow.show()
        self.htoWindow.ui.OK.clicked.connect(
            lambda: (
                self.setHtoArray(),
                self.htoWindow.close(),
                readDataWorker(input_mode, input_path)
            )
        )
        

    def setSsdResult(self):
        self.purified_df = classifier.purify_droplets(self.GMM_full_df, self.confidence_threshold)
        self.SSD_idx = classifier.obtain_SSD_list(self.purified_df, self.sample_num, self.extract_id_ary)

    def setPdfPlotHto(self):
        self.hto_name = str(self.plotOptionWindow.ui.hto_to_plot.currentText())

    def saveResult(self, full = True, ssd = False):
        def ssdSaveHelper(output_path):
            io.store_cellranger(self.full_df, self.SSD_idx, output_path)

        output_path = QFileDialog.getExistingDirectory(self, "Open a directory")
        if (output_path == ('')):
            return
        dlg = self.openDialog(text = "Saving...")
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

    def plot(self, plot_type):
        def plotHelper():
            if (self.plot_file_name == "tsne.png"):
                return
            self.plot_file_name = "tsne.png"
            plot.tsne_plot(self.GMM_df, self.GMM_full_df)
        def pdfPlotHelper():
            self.plot_file_name = f"pdf_{self.hto_name}.png"
            pixmap = QPixmap(os.path.join(self.tmp_path, self.plot_file_name))
            pixmap = pixmap.scaled(self.ui.label_plot.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.ui.label_plot.setPixmap(pixmap)

        def pdfPlotWorker():
            dlg = self.openDialog(text = "Plotting PDF, it may take a few seconds...")
            self.asyncFunc(
                func = pdfPlotHelper,
                after = lambda: (
                    dlg.setText("Done."),
                    dlg.setStandardButtons(QMessageBox.Ok)
                )
            )

        if (plot_type == "pdf"):
            self.plotOptionWindow = pdfPlotWindow(self, hto_array = self.hto_array)
            self.plotOptionWindow.show()
            self.plotOptionWindow.ui.OK.clicked.connect(
                lambda: (
                    self.setPdfPlotHto(),
                    self.plotOptionWindow.close(),
                    pdfPlotWorker()
                )
            )
        elif (plot_type == "tsne"):
            dlg = self.openDialog(text = "Plotting tSNE, it may take a few minutes...")
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

    def plotMenu(self, point):
        menu = QMenu(self)
        save_plot_action = QAction("Save plot as png", self)
        save_plot_action.triggered.connect(self.savePlot)
        menu.addAction(save_plot_action)
        menu.exec_(self.ui.label_plot.mapToGlobal(point))

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
        if (not self.plot_file_name):
            dlg = self.openDialog(
                title = "Warning", 
                text = "Please plot your data first.",
                buttonStyle = QMessageBox.Ok
            )
            return
        path = QFileDialog.getSaveFileName(self, "Save file", "", "*.png")
        if (path != ('','')):
            tmp_plot_path = os.path.join(self.tmp_path, self.plot_file_name)
            save_to_path = path[0]
            shutil.copyfile(tmp_plot_path, save_to_path)
            dlg = self.openDialog(
                title = "Success", 
                text = f"Plot saved to {save_to_path}.",
                buttonStyle = QMessageBox.Ok
            )

    def setThreshold(self):
        threshold = self.classifierWindow.ui.threshold.toPlainText()
        self.confidence_threshold = float(threshold)
        self.ui.threshold.setPlainText(threshold)

    def setSummary(self):
        total_num = self.estimatorWindow.ui.estimated_total_cell_num.toPlainText()
        self.estimated_total_cell_num = int(total_num)
        self.ui.total_num.setPlainText(total_num)

    def setExtract(self):
        self.extract_id_ary = self.classifierWindow.ui.hto_tags.toPlainText()
        if (self.extract_id_ary == ""):
            self.extract_id_ary = None
            return
        extract_id_ary = []
        tag_name_ary = []

        for tag_name in self.extract_id_ary.split(','):
            tag_name_ary.append(tag_name.split('+') )

        for tag_ary in tag_name_ary:
            mask = compute.init_mask(self.sample_num)
            for tag in tag_ary:
                hto_idx = self.hto_array.index(tag)
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
            self.setSsdResult()
        def runClassifierWorker():
            dlg = self.openDialog(text = "Running classifier...")
            self.asyncFunc(
                func = runClassifierHelper, 
                after = lambda: (
                        self.ui.tabWidget_console.setCurrentIndex(2),
                        # self.ui.classificationTable.setModel(pandasModel(self.GMM_full_df)),
                        # self.ui.classificationTable.resizeColumnsToContents(),
                        self.ui.classificationTable.setTableWidget(self.GMM_full_df),
                        dlg.setText("Done."),
                        dlg.setStandardButtons(QMessageBox.Ok),
                        self.ui.actionSave_MSM_free_results_to.setEnabled(True),
                        self.ui.actionSave_full_results_to.setEnabled(True),
                        self.ui.actionSave_simplified_results_to.setEnabled(True),
                        self.ui.actionPDF.setEnabled(True),
                        self.ui.actiontSNE.setEnabled(True),
                        self.ui.actionEstimate.setEnabled(True)
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

    def runEstimator(self):
        def runEstimatorHelper():
            result = estimator.estimator(
                self.GMM_full_df,
                self.purified_df,
                self.sample_num,
                self.base_bv_array,
                self.confidence_threshold,
                self.estimated_total_cell_num,
                self.SSD_idx,
                self.GMM_df.columns
            )
            self.estimateResult = result

        def setEstimationResult(full_report_dict):
            for (key, value) in full_report_dict.items():
                if ("rate" in key):
                    getattr(self.ui, key).setPlainText(str(value) + "%")
                else:
                    getattr(self.ui, key).setPlainText(str(value))

        def runEstimatorWorker():
            dlg = self.openDialog(text = "Running estimator...")
            self.asyncFunc(
                func = runEstimatorHelper,
                after = lambda: (
                    self.ui.tabWidget_console.setCurrentIndex(3),
                    setEstimationResult(self.estimateResult[0]),
                    self.ui.perSampleTable.setTableWidget(self.estimateResult[1]),
                    # self.ui.perSampleTable.setModel(pandasModel(self.estimateResult[1])),
                    self.ui.perSampleTable.resizeColumnsToContents(),
                    self.ui.perSampleTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch),
                    self.ui.perSampleTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch),
                    dlg.setText(
                        "GMM cannot find a viable solution that satisfies the droplet formation model. SSM rate estimation terminated." 
                        if (isinstance(self.estimateResult, int))
                        else "Done."
                    ),
                    dlg.setStandardButtons(QMessageBox.Ok),
                )
            )

        self.estimatorWindow = EstimatorWindow(self)
        self.estimatorWindow.show()
        self.estimatorWindow.ui.OK.clicked.connect(
            lambda: (
                self.setSummary(),
                self.estimatorWindow.close(),
                runEstimatorWorker()
            )
        )
        

def changeTheme(theme_type):
    file = QFile("./breeze/dist/" + theme_type + "/stylesheet.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    QApplication.instance().setStyleSheet(stream.readAll())


def main():
    dirname = os.path.dirname(PyQt5.__file__)
    plugin_path = os.path.join(dirname, 'Qt5', 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
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
    # mainWindow.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()