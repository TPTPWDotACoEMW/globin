# Form implementation generated from reading ui file 'addins_tab.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_AddinsTab(object):
    def setupUi(self, AddinsTab):
        AddinsTab.setObjectName("AddinsTab")
        AddinsTab.resize(893, 549)
        self.horizontalLayout = QtWidgets.QHBoxLayout(AddinsTab)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableViewAddins = QtWidgets.QTableView(parent=AddinsTab)
        self.tableViewAddins.setSortingEnabled(True)
        self.tableViewAddins.setObjectName("tableViewAddins")
        self.horizontalLayout.addWidget(self.tableViewAddins)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.buttonInstallNewAddin = QtWidgets.QToolButton(parent=AddinsTab)
        self.buttonInstallNewAddin.setMinimumSize(QtCore.QSize(180, 30))
        self.buttonInstallNewAddin.setObjectName("buttonInstallNewAddin")
        self.verticalLayout.addWidget(self.buttonInstallNewAddin)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(AddinsTab)
        QtCore.QMetaObject.connectSlotsByName(AddinsTab)

    def retranslateUi(self, AddinsTab):
        _translate = QtCore.QCoreApplication.translate
        AddinsTab.setWindowTitle(_translate("AddinsTab", "Form"))
        self.buttonInstallNewAddin.setText(_translate("AddinsTab", "Install New Addin"))