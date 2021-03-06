import sys
import os
import logging

ROOT_PATH = sys.path[0]
APP_PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(APP_PACKAGE_PATH)

import PyQt5
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QIcon
from app.controller import mainWindow
from app.stylesheet import breeze
from logging import getLogger
logger = getLogger(__name__)

def main():
    if (sys.platform == "win32"):
        import ctypes
        myappid = u'com.chp.genetics.gmmdemux'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    logger.info("GMM-demux started.")
    dirname = os.path.dirname(PyQt5.__file__)
    plugin_path = os.path.join(dirname, 'Qt5', 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
    app = QApplication(sys.argv)
    file = QFile(":/dark/stylesheet.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())
    app.setApplicationName('GMM Demux')
    app.setWindowIcon(QIcon('icon.ico'))
    main_window = mainWindow.MainWindow()
    sys.exit(app.exec_())