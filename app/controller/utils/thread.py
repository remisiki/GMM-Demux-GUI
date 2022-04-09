from PyQt5.QtCore import (
    QThread, 
    pyqtSignal, 
    QObject
)
import traceback

class Worker(QObject):
    finished = pyqtSignal(object)

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
        except Exception:
            self.finished.emit(traceback.format_exc())

def syncFun(func, args = None, callback = None):
    thread = QThread()
    worker = Worker(f = func, args = args)
    worker.moveToThread(thread)
    thread.started.connect(worker.func)
    worker.finished.connect(lambda e: thread.quit())
    worker.finished.connect(lambda e: worker.deleteLater())
    thread.finished.connect(thread.deleteLater)
    thread.start()
    if (callback):
        worker.finished.connect(lambda e: callback(e))