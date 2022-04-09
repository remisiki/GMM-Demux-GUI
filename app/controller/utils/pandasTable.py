import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

# class pandasModel(QAbstractTableModel):

#     def __init__(self, data):
#         QAbstractTableModel.__init__(self)
#         self._data = data
#         # self._data = data.reset_index()
#         # self._data = self._data.rename(columns = {'index': 'GEM'})

#     def rowCount(self, parent=None):
#         return self._data.shape[0]

#     def columnCount(self, parnet=None):
#         return self._data.shape[1]

#     def data(self, index, role=Qt.DisplayRole):
#         if index.isValid():
#             if role == Qt.DisplayRole:
#                 return str(self._data.iloc[index.row(), index.column()])
#         return None

#     def headerData(self, index, orientation, role):
#         if orientation == Qt.Horizontal and role == Qt.DisplayRole:
#             return self._data.columns[index]
#         if orientation == Qt.Vertical and role == Qt.DisplayRole:
#             return self._data.index[index]
#         return None

# def setTableView(table, data):
#     table.setModel(pandasModel(data))
#     table.resizeColumnsToContents()

# def add_method(cls):
#     def decorator(func):
#         @wraps(func) 
#         def wrapper(self, *args, **kwargs): 
#             return func(*args, **kwargs)
#         setattr(cls, func.__name__, wrapper)
#         # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
#         return func # returning func means func can still be used normally
#     return decorator

def setTableWidget(self, data):
    row_count = data.shape[0]
    column_count = data.shape[1]
    self.setRowCount(row_count)
    self.setColumnCount(column_count)
    for index, value in enumerate(data.columns):
        column = QTableWidgetItem(str(value))
        column.setToolTip(str(value))
        self.setHorizontalHeaderItem(index, column)
    for index, value in enumerate(data.index):
        row = QTableWidgetItem(str(value))
        row.setToolTip(str(value))
        self.setVerticalHeaderItem(index, row)
    for i in range(row_count):
        for j in range(column_count):
            cell_data = str(data.iat[i, j])
            cell = QTableWidgetItem(cell_data)
            cell.setToolTip(cell_data)
            self.setItem(i, j, cell)
    self.resizeColumnsToContents()
    self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    self.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

setattr(QTableWidget, 'setTableWidget', setTableWidget)