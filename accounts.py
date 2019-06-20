from PyQt5 import QtWidgets, QtCore

from PyQt5.QtWidgets import (
    QWidget,
    QSplashScreen,
    QDialog,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QApplication,
    QAction,
    QMainWindow,
    QStackedWidget,
    QFormLayout,
    QLineEdit,
)

from models import get_accounts
from tools import convert, add_to_table


def accounts_dialog(parent_, group=None, width=640, height=480):
    my_dialog = QDialog(parent_)
    my_dialog.setObjectName("Accounts dialog")
    _translate = QtCore.QCoreApplication.translate
    my_dialog.setWindowTitle(_translate("Accounts dialog", "Selecciona cuenta"))
    # size = my_dialog.size()
    # w = size.width()
    # h = size.height()

    t = QtWidgets.QTableWidget(my_dialog)
    t.setGeometry(QtCore.QRect(20, 100, width - 40, height - 100))
    t.setRowCount(0)
    t.setColumnCount(2)
    t.setHorizontalHeaderLabels((
        _translate("Accounts dialog", "Cuenta"),
        _translate("Accounts dialog", "Nombre")
    ))
    header = t.horizontalHeader()
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
    t.horizontalHeaderItem(0).setTextAlignment(QtCore.Qt.AlignHCenter)
    t.setObjectName("t")

    if group:
        accounts = get_accounts(lambda x: str(x.id)[0] == str(group))
    else:
        accounts = get_accounts()
    for account in accounts:
        add_to_table(t, convert(account.values()))

    my_dialog.exec_()
