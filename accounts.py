from PyQt5 import QtWidgets, QtCore, QtGui

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


class MyLineEdit(QLineEdit):
    keyPressed = QtCore.pyqtSignal(str)

    def keyPressEvent(self, event):
        super(MyLineEdit, self).keyPressEvent(event)
        t = self.text()
        if not t or len(t) > 2:
            self.keyPressed.emit(self.text())


class AccountTableWidget(QtWidgets.QTableWidget):
    cellEditingStarted = QtCore.pyqtSignal(int, int)

    def edit(self, index, trigger, event):
        result = super(AccountTableWidget, self).edit(index, trigger, event)
        if result:
            self.cellEditingStarted.emit(index.row(), index.column())
        return result


def accounts_dialog(parent_, group=None, width=640, height=480):
    group = str(group).strip() if group is not None else None

    my_dialog = QDialog(parent_)
    my_dialog.setObjectName("Accounts dialog")
    _translate = QtCore.QCoreApplication.translate
    my_dialog.setWindowTitle(_translate("Accounts dialog", "Select account"))
    # size = my_dialog.size()
    # w = size.width()
    # h = size.height()

    form = QWidget(my_dialog)
    form.setGeometry(QtCore.QRect(20, 20, width - 40, 100))
    # form.setObjectName("form")
    form_layout = QtWidgets.QFormLayout(form)
    form_layout.setContentsMargins(20, 20, 20, 20)
    form_layout.setObjectName("form_layout")
    search_label = QtWidgets.QLabel(form)
    search_label.setObjectName("search_label")
    search_label.setText(_translate("Accounts dialog", "Search"))
    form_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, search_label)
    search_edit = MyLineEdit(form)
    search_edit.setObjectName("search_edit")
    form_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, search_edit)

    t = QtWidgets.QTableWidget(my_dialog)
    t.setGeometry(QtCore.QRect(20, 100, width - 40, height))
    t.setRowCount(0)
    t.setColumnCount(2)
    t.setHorizontalHeaderLabels((
        _translate("Accounts dialog", "Code"),
        _translate("Accounts dialog", "Name")
    ))
    header = t.horizontalHeader()
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
    t.horizontalHeaderItem(0).setTextAlignment(QtCore.Qt.AlignHCenter)
    t.setObjectName("t")

    def updt_srch_value(strg):
        def fltr(srch, group):
            if group and srch:
                return lambda x: str(x.id)[0] == group and srch in x.name
            elif group:
                return lambda x: str(x.id)[0] == group
            elif srch:
                return lambda x: srch in x.name
            return lambda x: True
        pull_accounts_to_table(t, fltr(strg, group))

    search_edit.keyPressed.connect(updt_srch_value)

    if group:
        group = str(group).strip()
        # accounts = get_accounts(lambda x: str(x.id)[0] == group)
        pull_accounts_to_table(t, lambda x: str(x.id)[0] == group)
    else:
        # accounts = get_accounts()
        pull_accounts_to_table(t)
    # for account in accounts:
    #     add_to_table(t, convert(account.values()))

    my_dialog.exec_()


def pull_accounts_to_table(tbl, lbd=None):
    tbl.setRowCount(0)
    accounts = get_accounts(lbd)
    for account in accounts:
        add_to_table(tbl, convert(account.values()))
