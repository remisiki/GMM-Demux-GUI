# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './app/xml/gmmd.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1080, 720)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1080, 720))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_control = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_control.sizePolicy().hasHeightForWidth())
        self.frame_control.setSizePolicy(sizePolicy)
        self.frame_control.setMinimumSize(QtCore.QSize(505, 326))
        self.frame_control.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_control.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_control.setLineWidth(3)
        self.frame_control.setObjectName("frame_control")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_control)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.frame_control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.label_11 = QtWidgets.QLabel(self.tab_6)
        self.label_11.setGeometry(QtCore.QRect(10, 10, 141, 31))
        self.label_11.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.threshold = QtWidgets.QPlainTextEdit(self.tab_6)
        self.threshold.setGeometry(QtCore.QRect(170, 10, 91, 31))
        self.threshold.setFocusPolicy(QtCore.Qt.NoFocus)
        self.threshold.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.threshold.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.threshold.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.threshold.setReadOnly(True)
        self.threshold.setPlaceholderText("")
        self.threshold.setObjectName("threshold")
        self.label_12 = QtWidgets.QLabel(self.tab_6)
        self.label_12.setGeometry(QtCore.QRect(10, 50, 141, 31))
        self.label_12.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.GEM_num = QtWidgets.QPlainTextEdit(self.tab_6)
        self.GEM_num.setEnabled(True)
        self.GEM_num.setGeometry(QtCore.QRect(170, 50, 91, 31))
        self.GEM_num.setFocusPolicy(QtCore.Qt.NoFocus)
        self.GEM_num.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.GEM_num.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.GEM_num.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.GEM_num.setReadOnly(True)
        self.GEM_num.setPlainText("")
        self.GEM_num.setPlaceholderText("")
        self.GEM_num.setObjectName("GEM_num")
        self.label_13 = QtWidgets.QLabel(self.tab_6)
        self.label_13.setGeometry(QtCore.QRect(10, 90, 141, 31))
        self.label_13.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.sample_num = QtWidgets.QPlainTextEdit(self.tab_6)
        self.sample_num.setGeometry(QtCore.QRect(170, 90, 91, 31))
        self.sample_num.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sample_num.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sample_num.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sample_num.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.sample_num.setReadOnly(True)
        self.sample_num.setPlainText("")
        self.sample_num.setPlaceholderText("")
        self.sample_num.setObjectName("sample_num")
        self.droplet_num = QtWidgets.QPlainTextEdit(self.tab_6)
        self.droplet_num.setGeometry(QtCore.QRect(170, 170, 91, 31))
        self.droplet_num.setFocusPolicy(QtCore.Qt.NoFocus)
        self.droplet_num.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.droplet_num.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.droplet_num.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.droplet_num.setReadOnly(True)
        self.droplet_num.setPlainText("")
        self.droplet_num.setPlaceholderText("")
        self.droplet_num.setObjectName("droplet_num")
        self.label_14 = QtWidgets.QLabel(self.tab_6)
        self.label_14.setGeometry(QtCore.QRect(10, 170, 141, 31))
        self.label_14.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.cell_num = QtWidgets.QPlainTextEdit(self.tab_6)
        self.cell_num.setGeometry(QtCore.QRect(170, 210, 91, 31))
        self.cell_num.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cell_num.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.cell_num.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.cell_num.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.cell_num.setReadOnly(True)
        self.cell_num.setPlainText("")
        self.cell_num.setPlaceholderText("")
        self.cell_num.setObjectName("cell_num")
        self.label_15 = QtWidgets.QLabel(self.tab_6)
        self.label_15.setGeometry(QtCore.QRect(10, 210, 141, 31))
        self.label_15.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.total_num = QtWidgets.QPlainTextEdit(self.tab_6)
        self.total_num.setGeometry(QtCore.QRect(170, 130, 91, 31))
        self.total_num.setFocusPolicy(QtCore.Qt.NoFocus)
        self.total_num.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.total_num.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.total_num.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.total_num.setReadOnly(True)
        self.total_num.setPlainText("")
        self.total_num.setPlaceholderText("")
        self.total_num.setObjectName("total_num")
        self.label_16 = QtWidgets.QLabel(self.tab_6)
        self.label_16.setGeometry(QtCore.QRect(10, 130, 141, 31))
        self.label_16.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.capture_rate = QtWidgets.QPlainTextEdit(self.tab_6)
        self.capture_rate.setGeometry(QtCore.QRect(480, 10, 91, 31))
        self.capture_rate.setFocusPolicy(QtCore.Qt.NoFocus)
        self.capture_rate.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.capture_rate.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.capture_rate.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.capture_rate.setReadOnly(True)
        self.capture_rate.setPlainText("")
        self.capture_rate.setPlaceholderText("")
        self.capture_rate.setObjectName("capture_rate")
        self.label_17 = QtWidgets.QLabel(self.tab_6)
        self.label_17.setGeometry(QtCore.QRect(320, 10, 141, 31))
        self.label_17.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.singlet_rate = QtWidgets.QPlainTextEdit(self.tab_6)
        self.singlet_rate.setGeometry(QtCore.QRect(480, 50, 91, 31))
        self.singlet_rate.setFocusPolicy(QtCore.Qt.NoFocus)
        self.singlet_rate.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.singlet_rate.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.singlet_rate.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.singlet_rate.setReadOnly(True)
        self.singlet_rate.setPlainText("")
        self.singlet_rate.setPlaceholderText("")
        self.singlet_rate.setObjectName("singlet_rate")
        self.label_18 = QtWidgets.QLabel(self.tab_6)
        self.label_18.setGeometry(QtCore.QRect(320, 50, 141, 31))
        self.label_18.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_18.setObjectName("label_18")
        self.msm_rate = QtWidgets.QPlainTextEdit(self.tab_6)
        self.msm_rate.setGeometry(QtCore.QRect(480, 90, 91, 31))
        self.msm_rate.setFocusPolicy(QtCore.Qt.NoFocus)
        self.msm_rate.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.msm_rate.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.msm_rate.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.msm_rate.setReadOnly(True)
        self.msm_rate.setPlainText("")
        self.msm_rate.setPlaceholderText("")
        self.msm_rate.setObjectName("msm_rate")
        self.label_19 = QtWidgets.QLabel(self.tab_6)
        self.label_19.setGeometry(QtCore.QRect(320, 90, 141, 31))
        self.label_19.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_19.setObjectName("label_19")
        self.ssm_rate = QtWidgets.QPlainTextEdit(self.tab_6)
        self.ssm_rate.setGeometry(QtCore.QRect(480, 130, 91, 31))
        self.ssm_rate.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ssm_rate.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ssm_rate.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ssm_rate.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.ssm_rate.setReadOnly(True)
        self.ssm_rate.setPlainText("")
        self.ssm_rate.setOverwriteMode(False)
        self.ssm_rate.setPlaceholderText("")
        self.ssm_rate.setObjectName("ssm_rate")
        self.label_20 = QtWidgets.QLabel(self.tab_6)
        self.label_20.setGeometry(QtCore.QRect(320, 130, 141, 31))
        self.label_20.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName("label_20")
        self.negative_rate = QtWidgets.QPlainTextEdit(self.tab_6)
        self.negative_rate.setGeometry(QtCore.QRect(480, 170, 91, 31))
        self.negative_rate.setFocusPolicy(QtCore.Qt.NoFocus)
        self.negative_rate.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.negative_rate.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.negative_rate.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.negative_rate.setReadOnly(True)
        self.negative_rate.setPlainText("")
        self.negative_rate.setPlaceholderText("")
        self.negative_rate.setObjectName("negative_rate")
        self.label_22 = QtWidgets.QLabel(self.tab_6)
        self.label_22.setGeometry(QtCore.QRect(320, 170, 141, 31))
        self.label_22.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_22.setObjectName("label_22")
        self.unclear_rate = QtWidgets.QPlainTextEdit(self.tab_6)
        self.unclear_rate.setGeometry(QtCore.QRect(480, 210, 91, 31))
        self.unclear_rate.setFocusPolicy(QtCore.Qt.NoFocus)
        self.unclear_rate.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.unclear_rate.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.unclear_rate.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.unclear_rate.setReadOnly(True)
        self.unclear_rate.setPlainText("")
        self.unclear_rate.setPlaceholderText("")
        self.unclear_rate.setObjectName("unclear_rate")
        self.label_23 = QtWidgets.QLabel(self.tab_6)
        self.label_23.setGeometry(QtCore.QRect(320, 210, 141, 31))
        self.label_23.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_23.setObjectName("label_23")
        self.tabWidget.addTab(self.tab_6, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_control, 0, 0, 1, 1)
        self.frame_plot = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_plot.sizePolicy().hasHeightForWidth())
        self.frame_plot.setSizePolicy(sizePolicy)
        self.frame_plot.setMinimumSize(QtCore.QSize(426, 326))
        self.frame_plot.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_plot.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_plot.setObjectName("frame_plot")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_plot)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_plot = QtWidgets.QLabel(self.frame_plot)
        self.label_plot.setMinimumSize(QtCore.QSize(406, 306))
        self.label_plot.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.label_plot.setText("")
        self.label_plot.setScaledContents(False)
        self.label_plot.setAlignment(QtCore.Qt.AlignCenter)
        self.label_plot.setObjectName("label_plot")
        self.verticalLayout_2.addWidget(self.label_plot)
        self.gridLayout.addWidget(self.frame_plot, 0, 1, 1, 1)
        self.frame_buttons = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_buttons.sizePolicy().hasHeightForWidth())
        self.frame_buttons.setSizePolicy(sizePolicy)
        self.frame_buttons.setMinimumSize(QtCore.QSize(200, 0))
        self.frame_buttons.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_buttons.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_buttons.setObjectName("frame_buttons")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_buttons)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.read = QtWidgets.QPushButton(self.frame_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.read.sizePolicy().hasHeightForWidth())
        self.read.setSizePolicy(sizePolicy)
        self.read.setObjectName("read")
        self.verticalLayout.addWidget(self.read)
        self.classify = QtWidgets.QPushButton(self.frame_buttons)
        self.classify.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.classify.sizePolicy().hasHeightForWidth())
        self.classify.setSizePolicy(sizePolicy)
        self.classify.setObjectName("classify")
        self.verticalLayout.addWidget(self.classify)
        self.estimate = QtWidgets.QPushButton(self.frame_buttons)
        self.estimate.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.estimate.sizePolicy().hasHeightForWidth())
        self.estimate.setSizePolicy(sizePolicy)
        self.estimate.setObjectName("estimate")
        self.verticalLayout.addWidget(self.estimate)
        self.plot = QtWidgets.QPushButton(self.frame_buttons)
        self.plot.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot.sizePolicy().hasHeightForWidth())
        self.plot.setSizePolicy(sizePolicy)
        self.plot.setObjectName("plot")
        self.verticalLayout.addWidget(self.plot)
        self.exit = QtWidgets.QPushButton(self.frame_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exit.sizePolicy().hasHeightForWidth())
        self.exit.setSizePolicy(sizePolicy)
        self.exit.setObjectName("exit")
        self.verticalLayout.addWidget(self.exit)
        self.gridLayout.addWidget(self.frame_buttons, 1, 1, 1, 1)
        self.result_tab = QtWidgets.QTabWidget(self.centralwidget)
        self.result_tab.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.result_tab.setTabPosition(QtWidgets.QTabWidget.North)
        self.result_tab.setObjectName("result_tab")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_7)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.dataTable = QtWidgets.QTableWidget(self.tab_7)
        self.dataTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.dataTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.dataTable.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.dataTable.setObjectName("dataTable")
        self.dataTable.setColumnCount(0)
        self.dataTable.setRowCount(0)
        self.gridLayout_4.addWidget(self.dataTable, 0, 0, 1, 1)
        self.result_tab.addTab(self.tab_7, "")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_8)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.classificationTable = QtWidgets.QTableWidget(self.tab_8)
        self.classificationTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.classificationTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.classificationTable.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.classificationTable.setObjectName("classificationTable")
        self.classificationTable.setColumnCount(0)
        self.classificationTable.setRowCount(0)
        self.gridLayout_5.addWidget(self.classificationTable, 0, 0, 1, 1)
        self.result_tab.addTab(self.tab_8, "")
        self.tab_9 = QtWidgets.QWidget()
        self.tab_9.setObjectName("tab_9")
        self.perSampleTable = QtWidgets.QTableWidget(self.tab_9)
        self.perSampleTable.setGeometry(QtCore.QRect(6, 6, 841, 141))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.perSampleTable.sizePolicy().hasHeightForWidth())
        self.perSampleTable.setSizePolicy(sizePolicy)
        self.perSampleTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.perSampleTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.perSampleTable.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.perSampleTable.setGridStyle(QtCore.Qt.SolidLine)
        self.perSampleTable.setRowCount(3)
        self.perSampleTable.setColumnCount(5)
        self.perSampleTable.setObjectName("perSampleTable")
        self.perSampleTable.horizontalHeader().setCascadingSectionResizes(True)
        self.perSampleTable.verticalHeader().setCascadingSectionResizes(True)
        self.label_28 = QtWidgets.QLabel(self.tab_9)
        self.label_28.setGeometry(QtCore.QRect(330, 240, 141, 31))
        self.label_28.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_28.setObjectName("label_28")
        self.GEM_num_ex = QtWidgets.QPlainTextEdit(self.tab_9)
        self.GEM_num_ex.setEnabled(True)
        self.GEM_num_ex.setGeometry(QtCore.QRect(180, 200, 91, 31))
        self.GEM_num_ex.setFocusPolicy(QtCore.Qt.NoFocus)
        self.GEM_num_ex.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.GEM_num_ex.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.GEM_num_ex.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.GEM_num_ex.setReadOnly(True)
        self.GEM_num_ex.setPlainText("")
        self.GEM_num_ex.setPlaceholderText("")
        self.GEM_num_ex.setObjectName("GEM_num_ex")
        self.label_27 = QtWidgets.QLabel(self.tab_9)
        self.label_27.setGeometry(QtCore.QRect(330, 200, 141, 31))
        self.label_27.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_27.setObjectName("label_27")
        self.MSM_num_ex = QtWidgets.QPlainTextEdit(self.tab_9)
        self.MSM_num_ex.setEnabled(True)
        self.MSM_num_ex.setGeometry(QtCore.QRect(180, 240, 91, 31))
        self.MSM_num_ex.setFocusPolicy(QtCore.Qt.NoFocus)
        self.MSM_num_ex.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.MSM_num_ex.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.MSM_num_ex.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.MSM_num_ex.setReadOnly(True)
        self.MSM_num_ex.setPlainText("")
        self.MSM_num_ex.setPlaceholderText("")
        self.MSM_num_ex.setObjectName("MSM_num_ex")
        self.label_25 = QtWidgets.QLabel(self.tab_9)
        self.label_25.setGeometry(QtCore.QRect(20, 240, 141, 31))
        self.label_25.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_25.setObjectName("label_25")
        self.label_26 = QtWidgets.QLabel(self.tab_9)
        self.label_26.setGeometry(QtCore.QRect(330, 160, 141, 31))
        self.label_26.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_26.setObjectName("label_26")
        self.ambiguous_rate = QtWidgets.QPlainTextEdit(self.tab_9)
        self.ambiguous_rate.setEnabled(True)
        self.ambiguous_rate.setGeometry(QtCore.QRect(180, 160, 91, 31))
        self.ambiguous_rate.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ambiguous_rate.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ambiguous_rate.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ambiguous_rate.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.ambiguous_rate.setReadOnly(True)
        self.ambiguous_rate.setPlaceholderText("")
        self.ambiguous_rate.setObjectName("ambiguous_rate")
        self.cluster_type = QtWidgets.QPlainTextEdit(self.tab_9)
        self.cluster_type.setEnabled(True)
        self.cluster_type.setGeometry(QtCore.QRect(490, 240, 91, 31))
        self.cluster_type.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cluster_type.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.cluster_type.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.cluster_type.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.cluster_type.setReadOnly(True)
        self.cluster_type.setPlainText("")
        self.cluster_type.setPlaceholderText("")
        self.cluster_type.setObjectName("cluster_type")
        self.pure_p_value = QtWidgets.QPlainTextEdit(self.tab_9)
        self.pure_p_value.setEnabled(True)
        self.pure_p_value.setGeometry(QtCore.QRect(490, 200, 91, 31))
        self.pure_p_value.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pure_p_value.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.pure_p_value.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.pure_p_value.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.pure_p_value.setReadOnly(True)
        self.pure_p_value.setPlainText("")
        self.pure_p_value.setPlaceholderText("")
        self.pure_p_value.setObjectName("pure_p_value")
        self.label_24 = QtWidgets.QLabel(self.tab_9)
        self.label_24.setGeometry(QtCore.QRect(20, 200, 141, 31))
        self.label_24.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_24.setObjectName("label_24")
        self.phony_p_value = QtWidgets.QPlainTextEdit(self.tab_9)
        self.phony_p_value.setEnabled(True)
        self.phony_p_value.setGeometry(QtCore.QRect(490, 160, 91, 31))
        self.phony_p_value.setFocusPolicy(QtCore.Qt.NoFocus)
        self.phony_p_value.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.phony_p_value.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.phony_p_value.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.phony_p_value.setReadOnly(True)
        self.phony_p_value.setPlainText("")
        self.phony_p_value.setPlaceholderText("")
        self.phony_p_value.setObjectName("phony_p_value")
        self.label_21 = QtWidgets.QLabel(self.tab_9)
        self.label_21.setGeometry(QtCore.QRect(20, 160, 141, 31))
        self.label_21.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_21.setObjectName("label_21")
        self.result_tab.addTab(self.tab_9, "")
        self.gridLayout.addWidget(self.result_tab, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1080, 28))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuTheme = QtWidgets.QMenu(self.menuSettings)
        self.menuTheme.setObjectName("menuTheme")
        self.menuRun = QtWidgets.QMenu(self.menubar)
        self.menuRun.setObjectName("menuRun")
        self.menuPlot = QtWidgets.QMenu(self.menuRun)
        self.menuPlot.setObjectName("menuPlot")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAdd_file_from_directory = QtWidgets.QAction(MainWindow)
        self.actionAdd_file_from_directory.setObjectName("actionAdd_file_from_directory")
        self.actionAdd_file_from_csv = QtWidgets.QAction(MainWindow)
        self.actionAdd_file_from_csv.setObjectName("actionAdd_file_from_csv")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionLight = QtWidgets.QAction(MainWindow)
        self.actionLight.setObjectName("actionLight")
        self.actionDark = QtWidgets.QAction(MainWindow)
        self.actionDark.setObjectName("actionDark")
        self.actionAdd_full_report = QtWidgets.QAction(MainWindow)
        self.actionAdd_full_report.setEnabled(True)
        self.actionAdd_full_report.setObjectName("actionAdd_full_report")
        self.actionRun = QtWidgets.QAction(MainWindow)
        self.actionRun.setEnabled(False)
        self.actionRun.setObjectName("actionRun")
        self.actionClassify = QtWidgets.QAction(MainWindow)
        self.actionClassify.setEnabled(False)
        self.actionClassify.setObjectName("actionClassify")
        self.actionQuick_Read = QtWidgets.QAction(MainWindow)
        self.actionQuick_Read.setObjectName("actionQuick_Read")
        self.actionSave_full_results_to = QtWidgets.QAction(MainWindow)
        self.actionSave_full_results_to.setEnabled(False)
        self.actionSave_full_results_to.setObjectName("actionSave_full_results_to")
        self.actionSave_simplified_results_to = QtWidgets.QAction(MainWindow)
        self.actionSave_simplified_results_to.setEnabled(False)
        self.actionSave_simplified_results_to.setObjectName("actionSave_simplified_results_to")
        self.actionSave_MSM_free_results_to = QtWidgets.QAction(MainWindow)
        self.actionSave_MSM_free_results_to.setEnabled(False)
        self.actionSave_MSM_free_results_to.setObjectName("actionSave_MSM_free_results_to")
        self.actionEstimate = QtWidgets.QAction(MainWindow)
        self.actionEstimate.setEnabled(False)
        self.actionEstimate.setObjectName("actionEstimate")
        self.actionPDF = QtWidgets.QAction(MainWindow)
        self.actionPDF.setEnabled(False)
        self.actionPDF.setObjectName("actionPDF")
        self.actiontSNE = QtWidgets.QAction(MainWindow)
        self.actiontSNE.setEnabled(False)
        self.actiontSNE.setObjectName("actiontSNE")
        self.actionSave_summary_report = QtWidgets.QAction(MainWindow)
        self.actionSave_summary_report.setEnabled(False)
        self.actionSave_summary_report.setObjectName("actionSave_summary_report")
        self.actionDocumentation = QtWidgets.QAction(MainWindow)
        self.actionDocumentation.setObjectName("actionDocumentation")
        self.actionGithub = QtWidgets.QAction(MainWindow)
        self.actionGithub.setObjectName("actionGithub")
        self.actionVersion = QtWidgets.QAction(MainWindow)
        self.actionVersion.setObjectName("actionVersion")
        self.actionView_logs = QtWidgets.QAction(MainWindow)
        self.actionView_logs.setObjectName("actionView_logs")
        self.actionOpen_log_file_location = QtWidgets.QAction(MainWindow)
        self.actionOpen_log_file_location.setObjectName("actionOpen_log_file_location")
        self.menuFile.addAction(self.actionAdd_file_from_directory)
        self.menuFile.addAction(self.actionAdd_file_from_csv)
        self.menuFile.addAction(self.actionAdd_full_report)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_MSM_free_results_to)
        self.menuFile.addAction(self.actionSave_full_results_to)
        self.menuFile.addAction(self.actionSave_simplified_results_to)
        self.menuFile.addAction(self.actionSave_summary_report)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuTheme.addAction(self.actionLight)
        self.menuTheme.addAction(self.actionDark)
        self.menuSettings.addAction(self.menuTheme.menuAction())
        self.menuPlot.addAction(self.actionPDF)
        self.menuPlot.addAction(self.actiontSNE)
        self.menuRun.addAction(self.actionClassify)
        self.menuRun.addAction(self.actionEstimate)
        self.menuRun.addAction(self.menuPlot.menuAction())
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addAction(self.actionGithub)
        self.menuHelp.addAction(self.actionVersion)
        self.menuTools.addAction(self.actionView_logs)
        self.menuTools.addAction(self.actionOpen_log_file_location)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuRun.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.result_tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GMM Demux"))
        self.label_11.setText(_translate("MainWindow", "Threshold"))
        self.threshold.setToolTip(_translate("MainWindow", "default: 0.8"))
        self.threshold.setPlainText(_translate("MainWindow", "0.8"))
        self.label_12.setText(_translate("MainWindow", "GEM count"))
        self.label_13.setText(_translate("MainWindow", "Sample count"))
        self.label_14.setText(_translate("MainWindow", "Droplet count"))
        self.label_15.setText(_translate("MainWindow", "Cell count"))
        self.total_num.setToolTip(_translate("MainWindow", "default: 0.8"))
        self.label_16.setText(_translate("MainWindow", "Total cell count"))
        self.label_17.setText(_translate("MainWindow", "Capture rate"))
        self.label_18.setText(_translate("MainWindow", "Singlet rate"))
        self.label_19.setText(_translate("MainWindow", "MSM rate"))
        self.label_20.setText(_translate("MainWindow", "SSM rate"))
        self.label_22.setText(_translate("MainWindow", "Negative rate"))
        self.label_23.setText(_translate("MainWindow", "Unclear rate"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("MainWindow", "Data Summary"))
        self.read.setText(_translate("MainWindow", "Read"))
        self.classify.setText(_translate("MainWindow", "Classify"))
        self.estimate.setText(_translate("MainWindow", "Estimate"))
        self.plot.setText(_translate("MainWindow", "Plot"))
        self.exit.setText(_translate("MainWindow", "Exit"))
        self.result_tab.setTabText(self.result_tab.indexOf(self.tab_7), _translate("MainWindow", "GEM Data"))
        self.result_tab.setTabText(self.result_tab.indexOf(self.tab_8), _translate("MainWindow", "Classification Result"))
        self.label_28.setText(_translate("MainWindow", "Cluster type"))
        self.label_27.setText(_translate("MainWindow", "Pure-type P-value"))
        self.label_25.setText(_translate("MainWindow", "MSM count"))
        self.label_26.setText(_translate("MainWindow", "Phony-type P-value"))
        self.ambiguous_rate.setToolTip(_translate("MainWindow", "default: 0.05"))
        self.ambiguous_rate.setPlainText(_translate("MainWindow", "0.05"))
        self.label_24.setText(_translate("MainWindow", "GEM count"))
        self.label_21.setText(_translate("MainWindow", "Ambiguous rate"))
        self.result_tab.setTabText(self.result_tab.indexOf(self.tab_9), _translate("MainWindow", "Estimation Report"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuSettings.setTitle(_translate("MainWindow", "&Settings"))
        self.menuTheme.setTitle(_translate("MainWindow", "Theme"))
        self.menuRun.setTitle(_translate("MainWindow", "&Run"))
        self.menuPlot.setTitle(_translate("MainWindow", "Plot"))
        self.menuHelp.setTitle(_translate("MainWindow", "&Help"))
        self.menuTools.setTitle(_translate("MainWindow", "&Tools"))
        self.actionAdd_file_from_directory.setText(_translate("MainWindow", "Add mtx file directory"))
        self.actionAdd_file_from_csv.setText(_translate("MainWindow", "Add from csv"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionLight.setText(_translate("MainWindow", "Light"))
        self.actionDark.setText(_translate("MainWindow", "Dark"))
        self.actionAdd_full_report.setText(_translate("MainWindow", "Add full report"))
        self.actionRun.setText(_translate("MainWindow", "Run"))
        self.actionRun.setShortcut(_translate("MainWindow", "F5"))
        self.actionClassify.setText(_translate("MainWindow", "Classify"))
        self.actionClassify.setShortcut(_translate("MainWindow", "F6"))
        self.actionQuick_Read.setText(_translate("MainWindow", "Quick Read"))
        self.actionQuick_Read.setShortcut(_translate("MainWindow", "F4"))
        self.actionSave_full_results_to.setText(_translate("MainWindow", "Save full results..."))
        self.actionSave_simplified_results_to.setText(_translate("MainWindow", "Save simplified results..."))
        self.actionSave_MSM_free_results_to.setText(_translate("MainWindow", "Save MSM-free results..."))
        self.actionSave_MSM_free_results_to.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionEstimate.setText(_translate("MainWindow", "Estimate"))
        self.actionEstimate.setShortcut(_translate("MainWindow", "F8"))
        self.actionPDF.setText(_translate("MainWindow", "PDF"))
        self.actiontSNE.setText(_translate("MainWindow", "tSNE"))
        self.actiontSNE.setShortcut(_translate("MainWindow", "F7"))
        self.actionSave_summary_report.setText(_translate("MainWindow", "Save summary report..."))
        self.actionDocumentation.setText(_translate("MainWindow", "Documentation"))
        self.actionGithub.setText(_translate("MainWindow", "Github"))
        self.actionVersion.setText(_translate("MainWindow", "Version"))
        self.actionView_logs.setText(_translate("MainWindow", "View logs"))
        self.actionOpen_log_file_location.setText(_translate("MainWindow", "Open log file location"))
