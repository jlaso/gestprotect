from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
from settings import settings, save_settings

kind_of_servers = {
    'MySQL': 'QMYSQL',
    'Postgres': 'QPSQL',
}


class ConfigDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(QDialog, self).__init__(*args, **kwargs)
        self.setObjectName("ConfigDialog")
        self.resize(369, 238)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(10, 180, 341, 41))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(self)
        self.formLayoutWidget.setGeometry(QtCore.QRect(0, 0, 371, 171))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        # kind of server: MySQL, Postgres
        self.kindLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.kindLabel.setObjectName("kindLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.kindLabel)
        self.kindCombo = QtWidgets.QComboBox(self.formLayoutWidget)
        self.kindCombo.setObjectName("kindCombo")
        for k in kind_of_servers:
            self.kindCombo.addItem(k)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.kindCombo)

        # url of the DB server
        self.serverLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.serverLabel.setObjectName("serverLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.serverLabel)
        self.serverEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.serverEdit.setObjectName("serverEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.serverEdit)

        # port of the server
        self.portLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.portLabel.setObjectName("portLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.portLabel)
        self.portEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.portEdit.setObjectName("portEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.portEdit)

        # name of the database to use
        self.dbLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.dbLabel.setObjectName("dbLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.dbLabel)
        self.dbEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.dbEdit.setObjectName("dbEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.dbEdit)

        # name of the user with enough permissions on database
        self.userLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.userLabel.setObjectName("userLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.userLabel)
        self.userEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.userEdit.setObjectName("userEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.userEdit)

        # password of the user
        self.passwordLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.passwordLabel.setObjectName("passwordLabel")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.passwordLabel)
        self.passwordEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.passwordEdit.setObjectName("passwordEdit")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.passwordEdit)

        self.retranslateUi()

        try:
            self.kindCombo.setCurrentIndex(list(kind_of_servers.keys()).index(settings.value('DB_KIND')))
        except ValueError:
            pass

        self.serverEdit.setText(settings.value('DB_SERVER'))
        self.portEdit.setText(settings.value('DB_PORT'))
        self.dbEdit.setText(settings.value('DB_NAME'))
        self.userEdit.setText(settings.value('DB_USER'))
        self.passwordEdit.setText(settings.value('DB_PASSWORD'))

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def accept(self):
        print("OK")
        settings.setValue("DB_KIND", self.kindCombo.currentText())
        settings.setValue("DB_SERVER", self.serverEdit.text())
        settings.setValue("DB_PORT", self.portEdit.text())
        settings.setValue("DB_NAME", self.dbEdit.text())
        settings.setValue("DB_USER", self.userEdit.text())
        settings.setValue("DB_PASSWORD", self.passwordEdit.text())
        save_settings()
        super().accept()

    def reject(self):
        print("cancel")
        super().reject()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Configuración del servidor de BBDD"))
        self.kindLabel.setText(_translate("Dialog", "TIPO"))
        self.serverLabel.setText(_translate("Dialog", "SERVIDOR"))
        self.portLabel.setText(_translate("Dialog", "PUERTO"))
        self.dbLabel.setText(_translate("Dialog", "BASE DATOS"))
        self.userLabel.setText(_translate("Dialog", "USUARIO"))
        self.passwordLabel.setText(_translate("Dialog", "PASSWORD"))

