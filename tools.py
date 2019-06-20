from PyQt5 import QtCore, QtWidgets


def convert(in_data):
    def cvt(data):
        try:
            return ast.literal_eval(data)
        except Exception:
            return str(data)
    return tuple(map(cvt, in_data))


def add_to_table(table, data, editable=None):
    editable = [] if editable is None else editable
    row_position = table.rowCount()
    table.insertRow(row_position)
    table.is_not_edit = True
    for i, column in enumerate(data):
        item = QtWidgets.QTableWidgetItem(str(column))
        if i in editable:
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
        else:
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        table.setItem(row_position, i, item)
    table.is_not_edit = False
