from controller.init.gmmdWindow import Ui_MainWindow
import os
from gmmd import (
    compute, 
    estimator, 
    classifier, 
    io, 
    plot
)
import datetime
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QFileDialog, 
    QMessageBox, 
    QMenu, 
    QAction
)
from PyQt5.QtCore import (
    Qt, 
    QThread, 
    QFile, 
    QTextStream, 
    pyqtSignal, 
    QObject
)
from PyQt5.QtGui import QPixmap
from controller import (
    htoWindow, 
    classifierWindow, 
    estimatorWindow, 
    pdfPlotWindow
)
from controller.utils.pandasTable import *
import tempfile
import shutil
from logging import getLogger
import app.logger
import traceback

class Worker(QObject):
    finished = pyqtSignal(object)
    response = pyqtSignal(object)
    error = pyqtSignal(object)

    def __init__(self, f, args = None, parent = None):
        QThread.__init__(self, parent)
        self.f = f
        self.args = args

    def func(self):
        try:
            if (self.args):
                result = self.f(*self.args)
            else:
                result = self.f()
            self.finished.emit(None)
            self.response.emit(result)
        except Exception:
            self.finished.emit(traceback.format_exc())

class MainWindow(QMainWindow):
    tmp_path = os.path.join(tempfile.gettempdir(), ".gmm-demux")
    full_df = None
    GMM_df = None
    def __init__(self, parent=None):
        self.logger = getLogger("app").getChild(f"{__name__}.{__class__.__name__}")
        if (not os.path.exists(self.tmp_path)):
            os.makedirs(self.tmp_path)
            self.logger.info(f"Temp path not found, {self.tmp_path} created.")
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionAdd_file_from_directory.triggered.connect(lambda: self.readData(input_mode = "mtx"))
        self.ui.actionAdd_file_from_csv.triggered.connect(lambda: self.readData(input_mode = "csv"))
        self.ui.actionAdd_full_report.triggered.connect(lambda: self.readData(input_mode = "full"))
        self.ui.actionQuick_Read.triggered.connect(self.readData)
        self.ui.actionClassify.triggered.connect(self.runClassifier)
        self.ui.actionPDF.triggered.connect(lambda: self.plot(plot_type = "pdf"))
        self.ui.actiontSNE.triggered.connect(lambda: self.plot(plot_type = "tsne"))
        self.ui.actionSave_MSM_free_results_to.triggered.connect(lambda: self.saveResult("ssd"))
        self.ui.actionSave_full_results_to.triggered.connect(lambda: self.saveResult("full"))
        self.ui.actionSave_simplified_results_to.triggered.connect(lambda: self.saveResult("simple"))
        self.ui.actionSave_summary_report.triggered.connect(lambda: self.saveResult("summary"))
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
        self.ui.actionLight.triggered.connect(lambda: self.changeTheme("light"))
        self.ui.actionDark.triggered.connect(lambda: self.changeTheme("dark"))
        self.ui.statusbar.showMessage("Ready")
        self.ui.perSampleTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.perSampleTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.perSampleTable.setVerticalHeaderLabels(["Cell count", "SSD count", "Relative SSM rate"])
        self.ui.label_plot.customContextMenuRequested.connect(self.plotMenu)
        self.plot_file_name = None
        self.setFocus()
        self.logger.info("Intializing mainWindow finished.")
        self.show()

    def syncFun(self, func, args = None, callback = None):
        self.thread = QThread(self)
        self.worker = Worker(f = func, args = args)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.func)
        self.worker.finished.connect(lambda e: self.thread.quit())
        self.worker.finished.connect(lambda e: self.worker.deleteLater())
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        if (callback):
            self.worker.finished.connect(lambda e: callback(e))

    def errLogger(self, err, dlg = None, title = None, content = None):
        self.logger.error(err)
        if (dlg):
            if (title):
                dlg.setWindowTitle(title)
            else:
                dlg.setWindowTitle("Error")
            if (content):
                dlg.setText(content)
            else:
                dlg.setText("Error.")
            dlg.setStandardButtons(QMessageBox.Ok)

    def warnLogger(self, warning, dlg = None, title = None, content = None):
        self.logger.warning(warning)
        if (dlg):
            if (title):
                dlg.setWindowTitle(title)
            else:
                dlg.setWindowTitle("Warning")
            if (content):
                dlg.setText(content)
            else:
                dlg.setText("Warning.")
            dlg.setStandardButtons(QMessageBox.Ok)

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
                self.full_df, self.GMM_df = io.read_csv(input_path[0], hto_array)
            elif (input_mode == "full"):
                self.GMM_full_df, self.sample_num, self.class_name_ary, self.sample_names, self.confidence_threshold = classifier.read_full_classify_result(input_path)
                self.GEM_num = self.GMM_full_df.shape[0]
                self.base_bv_array = compute.obtain_base_bv_array(self.sample_num)
                self.purified_df = classifier.purify_droplets(self.GMM_full_df, self.confidence_threshold)
                self.SSD_idx = classifier.obtain_SSD_list(self.purified_df, self.sample_num)
                return

            self.GEM_num = self.GMM_df.shape[0]
            self.sample_num = self.GMM_df.shape[1]
            self.base_bv_array = compute.obtain_base_bv_array(self.sample_num)
            self.sample_names = self.GMM_df.columns

        def readDataWorker(input_mode, input_path):
            dlg = self.openDialog(text = "Reading data...")
            self.syncFun(
                func = readDataHelper, 
                args = [
                    input_mode,
                    input_path, 
                    self.hto_array
                ],
                callback = lambda e: readDataCallback(e, input_mode, dlg)
            )

        def readDataCallback(err, input_mode, dlg):
            if (err):
                self.errLogger(err, dlg)
                return
            if (input_mode == "full"):
                self.ui.tabWidget_console.setCurrentIndex(1)
                self.ui.GEM_num.setPlainText(str(self.GEM_num))
                self.ui.sample_num.setPlainText(str(self.sample_num))
                self.ui.classificationTable.setTableWidget(self.GMM_full_df)
                dlg.setText("Done.")
                dlg.setStandardButtons(QMessageBox.Ok)
                self.ui.actionEstimate.setEnabled(True)
                self.ui.estimate.setEnabled(True)
                self.ui.actionSave_full_results_to.setEnabled(True)
                self.ui.actionSave_simplified_results_to.setEnabled(True)
            else:
                self.ui.tabWidget_console.setCurrentIndex(0)
                self.ui.GEM_num.setPlainText(str(self.GEM_num))
                self.ui.sample_num.setPlainText(str(self.sample_num))
                self.ui.dataTable.setTableWidget(self.full_df)
                dlg.setText("Done.")
                dlg.setStandardButtons(QMessageBox.Ok)
                self.ui.actionClassify.setEnabled(True)
                self.ui.classify.setEnabled(True)

        if (input_mode == "mtx"):
            input_path = QFileDialog.getExistingDirectory(self, "Open a directory")
            if (input_path == ('')):
                return
        elif (input_mode == "csv"):
            input_path = QFileDialog.getOpenFileName(self, "Open a csv file", "", "*.csv")
            if (input_path == ('','')):
                return
        elif (input_mode == "full"):
            input_path = QFileDialog.getExistingDirectory(self, "Open a directory")
            if (input_path == ('')):
                return
        elif (not input_mode):
            input_path = r"/run/media/setsunayyw/0D7D06240D7D0624/SJTU/2021-09/研究/GMM-Demux-GUI/example_input/outs/filtered_feature_bc_matrix"

        self.logger.info(f"Reading data from {input_path}, mode: {input_mode}.")

        self.htoWindow = htoWindow.HtoWindow(self)
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

    def saveResult(self, save_mode = "full"):
        def ssdSaveHelper(output_path):
            io.store_cellranger(self.full_df, self.SSD_idx, output_path)

        def saveCallback(err, dlg, content):
            if (err):
                self.errLogger(err, dlg)
                return
            self.logger.info(content)
            dlg.setText(content),
            dlg.setStandardButtons(QMessageBox.Ok)

        output_path = QFileDialog.getExistingDirectory(self, "Open a directory")
        if (output_path == ('')):
            return
        dlg = self.openDialog(text = "Saving...")
        if (save_mode == "ssd"):
            self.syncFun(
                func = ssdSaveHelper,
                args = [
                    output_path
                ],
                callback = lambda e: saveCallback(e, dlg, f"MSM-free results stored to {output_path}.")
            )
        elif (save_mode == "full"):
            self.syncFun(
                func = classifier.store_full_classify_result,
                args = [
                    self.GMM_full_df,
                    self.class_name_ary,
                    self.confidence_threshold,
                    output_path
                ],
                callback = lambda e: saveCallback(e, dlg, f"Full report stored to {output_path}.")
            )
        elif (save_mode == "simple"):
            self.syncFun(
                func = classifier.store_simplified_classify_result,
                args = [
                    self.GMM_full_df,
                    self.class_name_ary,
                    output_path,
                    self.sample_num,
                    self.confidence_threshold
                ],
                callback = lambda e: saveCallback(e, dlg, f"Simplified report stored to {output_path}.")
            )
        elif (save_mode == "summary"):
            summary_report_path = os.path.join(output_path, 'GMM_summary_report.txt')
            self.syncFun(
                func = estimator.store_summary_result,
                args = [
                    summary_report_path,
                    self.estimate_result[0],
                    self.estimate_result[1]
                ],
                callback = lambda e: saveCallback(e, dlg, f"Summary report stored to {summary_report_path}.")
            )

    def plot(self, plot_type):
        def plotHelper():
            self.plot_file_name = "tsne.png"
            plot.tsne_plot(self.GMM_df, self.GMM_full_df)

        def pdfPlotHelper():
            self.plot_file_name = f"pdf_{self.hto_name}.png"
            pixmap = QPixmap(os.path.join(self.tmp_path, self.plot_file_name))
            pixmap = pixmap.scaled(self.ui.label_plot.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.ui.label_plot.setPixmap(pixmap)

        def pdfPlotWorker():
            dlg = self.openDialog(text = "Plotting PDF, it may take a few seconds...")
            self.syncFun(
                func = pdfPlotHelper,
                callback = lambda e: pdfPlotCallback(e, dlg)
            )

        def pdfPlotCallback(err, dlg):
            if (err):
                self.errLogger(err, dlg)
                return
            dlg.setText("Done.")
            dlg.setStandardButtons(QMessageBox.Ok)

        def tsnePlotCallback(err, dlg):
            if (err):
                self.errLogger(err, dlg)
                return
            self.ui.label_plot.setPixmap(
                QPixmap(os.path.join(self.tmp_path, "tsne.png")).scaled(self.ui.label_plot.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
            dlg.setText("Done.")
            dlg.setStandardButtons(QMessageBox.Ok)

        self.logger.info(f"Plot function called, type: {plot_type}.")
        if (plot_type == "pdf"):
            self.plotOptionWindow = pdfPlotWindow.pdfPlotWindow(self, hto_array = self.hto_array)
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
            self.syncFun(
                func = plotHelper,
                callback = lambda e: tsnePlotCallback(e, dlg)
            )

    def plotMenu(self, point):
        menu = QMenu(self)
        save_plot_action = QAction("Save plot as png", self)
        view_plot_action = QAction("Open with system viewer", self)
        save_plot_action.triggered.connect(self.savePlot)
        view_plot_action.triggered.connect(self.openPlot)
        menu.addAction(view_plot_action)
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
        if (self.plot_file_name):
            pixmap = QPixmap(os.path.join(self.tmp_path, self.plot_file_name))
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

    def openPlot(self):
        if (not self.plot_file_name):
            dlg = self.openDialog(
                title = "Warning", 
                text = "Please plot your data first.",
                buttonStyle = QMessageBox.Ok
            )
            return
        path = os.path.join(self.tmp_path, self.plot_file_name)
        if (not os.path.isfile(path)):
            dlg = self.openDialog(
                title = "Error", 
                text = "Error may have occured during plotting, please check log file.",
                buttonStyle = QMessageBox.Ok
            )
            return
        plot.openImage(path)

    def setThreshold(self):
        threshold = self.classifierWindow.ui.threshold.toPlainText()
        self.confidence_threshold = float(threshold)
        self.ui.threshold.setPlainText(threshold)

    def setSummary(self):
        total_num = self.estimatorWindow.ui.estimated_total_cell_num.toPlainText()
        self.examine_cell_path = self.estimatorWindow.ui.examine_cell_path.toPlainText()
        self.ambiguous_rate = self.estimatorWindow.ui.ambiguous_rate.toPlainText()
        self.ambiguous_rate = float(self.ambiguous_rate)
        try:
            self.estimated_total_cell_num = int(total_num)
        except:
            self.estimated_total_cell_num = None
            return

        self.ui.total_num.setPlainText(total_num)

    def setExtract(self):
        self.extract_id_ary = []
        extract_id_ary = []
        tag_name_ary = []
        for index in range(self.classifierWindow.ui.hto_tags.count()):
            item = self.classifierWindow.ui.hto_tags.item(index)
            extract_id_ary.append(item.text())
        if (not extract_id_ary):
            self.extract_id_ary = None
            return
        for tag_name in extract_id_ary:
            tag_name_ary.append(tag_name.split('+'))
        for tag_ary in tag_name_ary:
            mask = compute.init_mask(self.sample_num)
            for tag in tag_ary:
                hto_idx = self.hto_array.index(tag)
                bv = compute.set_bit(mask, hto_idx)

            for idx in range(0, len(self.base_bv_array)):
                if self.base_bv_array[idx] == mask:
                    extract_id = idx

            self.extract_id_ary.append(extract_id)
            self.extract_id_ary = list(set(self.extract_id_ary))

    def runClassifier(self):
        def runClassifierHelper():
            self.logger.info(f"Classifier called.")
            high_array, low_array = classifier.obtain_arrays(self.GMM_df, self.tmp_path)
            self.GMM_full_df, self.class_name_ary = classifier.classify_drops(self.base_bv_array, high_array, low_array, self.GMM_df)
            self.setSsdResult()
        def runClassifierWorker():
            dlg = self.openDialog(text = "Running classifier...")
            self.syncFun(
                func = runClassifierHelper, 
                callback = lambda e: classifierCallback(e, dlg)
            )

        def classifierCallback(err, dlg):
            if (err):
                self.errLogger(err, dlg)
                return
            self.ui.tabWidget_console.setCurrentIndex(1)
            # self.ui.classificationTable.setModel(pandasModel(self.GMM_full_df))
            # self.ui.classificationTable.resizeColumnsToContents()
            self.ui.classificationTable.setTableWidget(self.GMM_full_df)
            dlg.setText("Done.")
            dlg.setStandardButtons(QMessageBox.Ok)
            self.ui.actionSave_MSM_free_results_to.setEnabled(True)
            self.ui.actionSave_full_results_to.setEnabled(True)
            self.ui.actionSave_simplified_results_to.setEnabled(True)
            self.ui.actionPDF.setEnabled(True)
            self.ui.actiontSNE.setEnabled(True)
            self.ui.actionEstimate.setEnabled(True if (not self.extract_id_ary) else False)
            self.ui.estimate.setEnabled(True if (not self.extract_id_ary) else False)

        self.classifierWindow = classifierWindow.ClassifierWindow(self)
        self.classifierWindow.show()
        self.classifierWindow.setList(self.hto_array)
        self.classifierWindow.ui.add.clicked.connect(self.classifierWindow.addHto)
        self.classifierWindow.ui.remove.clicked.connect(self.classifierWindow.removeHto)
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
            estimate_result = estimator.estimator(
                self.GMM_full_df,
                self.purified_df,
                self.sample_num,
                self.base_bv_array,
                self.confidence_threshold,
                self.estimated_total_cell_num,
                self.SSD_idx,
                self.sample_names,
                self.examine_cell_path,
                self.ambiguous_rate,
                self.class_name_ary
            )
            self.estimate_result = estimate_result

        def setEstimationResult(full_report_dict):
            for (key, value) in full_report_dict.items():
                if ("rate" in key):
                    getattr(self.ui, key).setPlainText(str(value) + "%")
                else:
                    getattr(self.ui, key).setPlainText(str(value))

        def estimatorCallback(err, dlg):
            if (err):
                self.errLogger(err, dlg)
                return
            if (isinstance(self.estimate_result, int)):
                self.warnLogger("SSM-rate estimation terminated.", dlg, content = "GMM cannot find a viable solution that satisfies the droplet formation model. SSM rate estimation terminated.")
                return
            self.ui.tabWidget_console.setCurrentIndex(2)
            setEstimationResult(self.estimate_result[2])
            self.ui.perSampleTable.setTableWidget(self.estimate_result[1])
            # self.ui.perSampleTable.setModel(pandasModel(self.estimate_result[1]))
            self.ui.perSampleTable.resizeColumnsToContents()
            self.ui.perSampleTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.ui.perSampleTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            GEM_num, MSM_num, phony_test_pvalue, pure_test_pvalue, cluster_type = self.estimate_result[3]
            self.ui.ambiguous_rate.setPlainText(str(self.ambiguous_rate))
            self.ui.GEM_num_ex.setPlainText(str(GEM_num))
            self.ui.MSM_num_ex.setPlainText(str(MSM_num))
            self.ui.phony_p_value.setPlainText(f"{phony_test_pvalue:.2e}")
            self.ui.pure_p_value.setPlainText(f"{pure_test_pvalue:.2e}")
            self.ui.cluster_type.setPlainText(cluster_type)
            dlg.setText(
                "Done."
            )
            dlg.setStandardButtons(QMessageBox.Ok)
            self.ui.actionSave_summary_report.setEnabled(True)
        def runEstimatorWorker():
            dlg = self.openDialog(text = "Running estimator...")
            self.syncFun(
                func = runEstimatorHelper,
                callback = lambda e: estimatorCallback(e, dlg)
            )

        self.estimatorWindow = estimatorWindow.EstimatorWindow(self)
        self.estimatorWindow.show()
        self.estimatorWindow.ui.OK.clicked.connect(
            lambda: (
                self.setSummary(),
                self.estimatorWindow.close(),
                runEstimatorWorker()
            )
        )

    def changeTheme(self, theme_type):
        file = QFile(f":/{theme_type}/stylesheet.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        QApplication.instance().setStyleSheet(stream.readAll())