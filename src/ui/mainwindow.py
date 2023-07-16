# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(817, 600)
        self.centralWidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabAddinsInfo = AddinsTab()
        self.tabAddinsInfo.setObjectName("tabAddinsInfo")
        self.tabWidget.addTab(self.tabAddinsInfo, "")
        self.tabOptions = OptionsTab()
        self.tabOptions.setObjectName("tabOptions")
        self.tabWidget.addTab(self.tabOptions, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.buttonSave = QtWidgets.QToolButton(parent=self.centralWidget)
        self.buttonSave.setMinimumSize(QtCore.QSize(100, 30))
        self.buttonSave.setObjectName("buttonSave")
        self.horizontalLayout_2.addWidget(self.buttonSave)
        self.buttonSaveAndLaunch = QtWidgets.QToolButton(parent=self.centralWidget)
        self.buttonSaveAndLaunch.setMinimumSize(QtCore.QSize(180, 30))
        self.buttonSaveAndLaunch.setObjectName("buttonSaveAndLaunch")
        self.horizontalLayout_2.addWidget(self.buttonSaveAndLaunch)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 817, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAddinsInfo), _translate("MainWindow", "Addins"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabOptions), _translate("MainWindow", "Options"))
        self.buttonSave.setText(_translate("MainWindow", "Save"))
        self.buttonSaveAndLaunch.setText(_translate("MainWindow", "Save and launch World Of Goo!"))
from src.ui_addins_tab import AddinsTab
from src.ui_options_tab import OptionsTab