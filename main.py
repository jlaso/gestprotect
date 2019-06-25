from time import time, sleep
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
# from db import db
# from PyQt5.QtCore import QSettings
# from PyQt5.QtCore import Qt
# from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtGui import QIcon, QPixmap
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
from config_dialog import ConfigDialog
from settings import settings
from models import *
from accounts import accounts_dialog, AccountTableWidget
from tools import convert, add_to_table

app = None

MAIN_MENU_WIN = 0
ACCOUNTS_WIN = 1
DIARY_WIN = 2
BALANCE_WIN = 3
CPPGG_WIN = 4
CONFIG_WIN = 5

WIDTH = 800
HEIGHT = 600


class MainWindow(QMainWindow):
    accountsTable = None

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.resize(WIDTH, HEIGHT)
        self.window = 0
        self.last_edit = None
        self.config_dialog = ConfigDialog()

        self._translate = QtCore.QCoreApplication.translate

        self.setWindowTitle(self._translate("MainWindow", "Contabilidad Asociación"))
        central_widget = QtWidgets.QWidget(self)
        central_widget.setObjectName("central_widget")
        # size policy
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(central_widget.sizePolicy().hasHeightForWidth())
        central_widget.setSizePolicy(size_policy)

        self.statusBar = QtWidgets.QStatusBar(self)
        self.statusBar.setObjectName("statusBar")
        self.setStatusBar(self.statusBar)

        # stacked windows
        self.Stack = QStackedWidget(central_widget)
        self.Stack.setGeometry(self.geometry())
        self.Stack.setObjectName("Stack")
        self.main_menu_stack = self.main_menu_view()
        self.Stack.addWidget(self.main_menu_stack)
        self.Stack.addWidget(self.accounts_view())

        self.setCentralWidget(central_widget)
        self.display(MAIN_MENU_WIN)
        self.show()
        self.show_sb_msg("Ready...")

    def show_sb_msg(self, msg):
        self.statusBar.showMessage(msg)

    def gen_big_button(self, from_widget, to_layout, btn_name, text, row, col,
                       min_w=0, min_h=100, point_size=27, weight=75, bold=True,
                       color="#1976D2", rows=1, cols=1):
        btn = QtWidgets.QPushButton(from_widget)
        btn.setMinimumSize(QtCore.QSize(min_w, min_h))
        font = QtGui.QFont()
        font.setPointSize(point_size)
        font.setBold(bold)
        font.setWeight(weight)
        btn.setFont(font)
        btn.setStyleSheet("QPushButton { color: %s; }" % color)
        btn.setObjectName(btn_name)
        btn.setText(self._translate(btn_name, text))
        # btn.setShortcut(_translate("MainWindow", "D"))
        to_layout.addWidget(btn, row, col, rows, cols)
        return btn

    def gen_little_button(self, from_widget, to_layout, btn_name, text, row, col,
                          min_w=0, min_h=50, point_size=17, weight=55, bold=False,
                          color="#1976D2", rows=1, cols=1):
        btn = QtWidgets.QPushButton(from_widget)
        btn.setMinimumSize(QtCore.QSize(min_w, min_h))
        font = QtGui.QFont()
        font.setPointSize(point_size)
        font.setBold(bold)
        font.setWeight(weight)
        btn.setFont(font)
        btn.setStyleSheet("QPushButton { color: %s; }" % color)
        btn.setObjectName(btn_name)
        btn.setText(self._translate(btn_name, text))
        # btn.setShortcut(_translate("MainWindow", "D"))
        to_layout.addWidget(btn, row, col, rows, cols)
        return btn

    def create_account(self):
        # print("btn pressed ", self.name_edit.text())
        try:
            db.add_account(
                id=self.code_edit.text(),
                name=self.name_edit.text(),
            )
        except Exception as e:
            print(repr(e))
            self.show_sb_msg("DB Insert Error")

    def accounts_view(self):
        page = QWidget()

        layout = QVBoxLayout()
        # layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(6)
        layout.setObjectName("layout")
        page.setLayout(layout)

        # size = page.size()
        w = WIDTH  # size.width()
        h = HEIGHT  # size.height()
        print("size is %dx%d" % (w, h))

        form = QWidget(page)
        form.setGeometry(QtCore.QRect(20, 20, w - 40, 100))
        # form.setObjectName("form")
        form_layout = QtWidgets.QFormLayout(form)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setObjectName("form_layout")

        code_label = QtWidgets.QLabel(form)
        code_label.setObjectName("code_label")
        code_label.setText(self._translate("Accounts", "Cuenta"))
        form_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, code_label)
        self.code_edit = QtWidgets.QLineEdit(form)
        self.code_edit.setObjectName("code_edit")
        form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.code_edit)
        name_label = QtWidgets.QLabel(form)
        name_label.setObjectName("name_label")
        name_label.setText(self._translate("Accounts", "Nombre"))
        form_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, name_label)
        self.name_edit = QtWidgets.QLineEdit(form)
        self.name_edit.setObjectName("name_edit")
        form_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.name_edit)
        add_btn = QtWidgets.QPushButton(form)
        add_btn.setObjectName("add_btn")
        add_btn.setText(self._translate("Accounts", "Crear"))
        form_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, add_btn)
        add_btn.released.connect(self.create_account)

        self.accountsTable = AccountTableWidget(page)
        self.accountsTable.setGeometry(QtCore.QRect(20, 100, w - 40, h - 100))
        self.accountsTable.setRowCount(0)
        self.accountsTable.setColumnCount(2)
        self.accountsTable.setHorizontalHeaderLabels(("Cuenta", "Nombre"))
        header = self.accountsTable.horizontalHeader()
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.accountsTable.horizontalHeaderItem(0).setTextAlignment(QtCore.Qt.AlignHCenter)
        self.accountsTable.setObjectName("accountsTable")
        self.accountsTable.cellEditingStarted.connect(self.edit_account)
        self.accountsTable.cellChanged.connect(self.end_edit_account)

        table_layout = QVBoxLayout(self.accountsTable)
        table_layout.setContentsMargins(20, 20, 20, 20)
        table_layout.setObjectName("table_layout")

        return page

    def main_menu_view(self):
        page = QWidget()
        vert_layout = QtWidgets.QVBoxLayout()
        vert_layout.setContentsMargins(51, 51, 51, 51)
        vert_layout.setSpacing(6)
        vert_layout.setObjectName("vert_layout")

        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setSpacing(6)
        grid_layout.setObjectName("grid_layout")

        spacer_item_top = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        grid_layout.addItem(spacer_item_top, 0, 0, 1, 1)
        account_button = self.gen_big_button(page, grid_layout, "account_button",
                                             self._translate("menu", "Accounts"), 1, 0)
        diary_button = self.gen_big_button(page, grid_layout, "diary_button",
                                           self._translate("menu", "Accounting journal"), 1, 1)
        balance_button = self.gen_big_button(page, grid_layout, "balance_button",
                                             self._translate("menu", "Balance sheet"), 2, 0)
        cppgg_button = self.gen_big_button(page, grid_layout, "cppgg_button",
                                           self._translate("menu", "Profit and loss account"), 2, 1)
        exit_button = self.gen_big_button(page, grid_layout, "exit_button",
                                          self._translate("menu", "Exit"), 3, 0, cols=2)
        spacer_item_bottom = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                                   QtWidgets.QSizePolicy.Expanding)
        grid_layout.addItem(spacer_item_bottom, 4, 0, 1, 1)
        config_button = self.gen_little_button(page, grid_layout, "config_button",
                                               self._translate("menu", "Setup"), 6, 0)

        exit_button.pressed.connect(lambda: app.quit())
        account_button.pressed.connect(lambda: self.display(ACCOUNTS_WIN))
        diary_button.pressed.connect(lambda: self.display(DIARY_WIN))
        balance_button.pressed.connect(lambda: self.display(BALANCE_WIN))
        cppgg_button.pressed.connect(lambda: self.display(CPPGG_WIN))
        config_button.pressed.connect(lambda: self.config_dialog.show())

        vert_layout.addLayout(grid_layout)
        page.setLayout(vert_layout)

        return page

    def edit_account(self, row, col):
        data = self.accountsTable.cellWidget(row, col)
        self.last_edit = data.text()
        # row = mi.row()
        # column = mi.column()
        # id_ = self.accountsTable.item(row, 0)
        # print("edit_account %s %s" % (row, col))
        # print(repr(id_.text()))

    def end_edit_account(self, row, col):
        if self.accountsTable.is_not_edit:
            pass
        else:
            data = self.accountsTable.cellWidget(row, col)
            # print("end_edit_account %d %d" % (row, col))
            _name = data.text()
            _id = self.accountsTable.item(row, 0).text()
            # print(_id, _name)
            change_account(id=_id, name=_name)

    def display(self, i):
        self.window = i
        self.Stack.setCurrentIndex(i)
        if i == CONFIG_WIN:
            ConfigDialog().show()

        if i == ACCOUNTS_WIN:
            self.accountsTable.setRowCount(0)
            # accounts = db.get_accounts()
            accounts = get_accounts()
            for account in accounts:
                add_to_table(self.accountsTable,
                             convert(account.values()),
                             editable=[1])
            self.show_sb_msg("Accounts read Done. %d" % len(accounts))
            return

        if i == DIARY_WIN:
            print("value returned from accounts dialog is", accounts_dialog(self, group=7))
            self.display(MAIN_MENU_WIN)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            if self.window == 0:
                self.close()
            else:
                self.display(0)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    start = time()
    splash = QSplashScreen(QPixmap("splash-screen.png"))
    splash.show()
    if time() - start < 1:
        sleep(1)

    translator = QtCore.QTranslator()
    translator.load("translations/es_ES.qm")
    app.installTranslator(translator)

    menu_window = MainWindow()
    menu_window.show()
    splash.finish(menu_window)

    if not settings.value('DB_SERVER'):  # or not db.open():
        menu_window.config_dialog.show()

    kind = settings.value('DB_KIND', 'sqlite')
    server = settings.value('DB_SERVER', 'database.sqlite')
    _db = settings.value('DB_NAME', None)
    user = settings.value('DB_USER', None)
    password = settings.value('DB_PASSWORD', None)

    if kind == 'sqlite':
        db.bind(provider='sqlite', filename=server, create_db=True)
    else:
        db.bind(provider=kind.lower(), user=user, password=password, host=server, database=_db)

    # sql_debug(True)
    db.generate_mapping(create_tables=True)

    sys.exit(app.exec_())
