# Form implementation generated from reading ui file 'profile_tab.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ProfileTab(object):
    def setupUi(self, ProfileTab):
        ProfileTab.setObjectName("ProfileTab")
        ProfileTab.resize(819, 646)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(ProfileTab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBoxProfiles = QtWidgets.QComboBox(parent=ProfileTab)
        self.comboBoxProfiles.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBoxProfiles.setObjectName("comboBoxProfiles")
        self.horizontalLayout.addWidget(self.comboBoxProfiles)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.stackedWidgetProfiles = QtWidgets.QStackedWidget(parent=ProfileTab)
        self.stackedWidgetProfiles.setObjectName("stackedWidgetProfiles")
        self.pageNoProfileFound = QtWidgets.QWidget()
        self.pageNoProfileFound.setObjectName("pageNoProfileFound")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.pageNoProfileFound)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelNoProfileFound = QtWidgets.QLabel(parent=self.pageNoProfileFound)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelNoProfileFound.setFont(font)
        self.labelNoProfileFound.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelNoProfileFound.setObjectName("labelNoProfileFound")
        self.horizontalLayout_2.addWidget(self.labelNoProfileFound)
        self.stackedWidgetProfiles.addWidget(self.pageNoProfileFound)
        self.pageProfileInfo = QtWidgets.QWidget()
        self.pageProfileInfo.setObjectName("pageProfileInfo")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.pageProfileInfo)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(5)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBoxLevels = QtWidgets.QGroupBox(parent=self.pageProfileInfo)
        self.groupBoxLevels.setObjectName("groupBoxLevels")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBoxLevels)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tableLevelsInfo = QtWidgets.QTableView(parent=self.groupBoxLevels)
        self.tableLevelsInfo.setSortingEnabled(True)
        self.tableLevelsInfo.setObjectName("tableLevelsInfo")
        self.tableLevelsInfo.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_3.addWidget(self.tableLevelsInfo)
        self.gridLayout_3.addWidget(self.groupBoxLevels, 0, 0, 2, 1)
        self.groupBoxProfile = QtWidgets.QGroupBox(parent=self.pageProfileInfo)
        self.groupBoxProfile.setObjectName("groupBoxProfile")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBoxProfile)
        self.gridLayout_4.setContentsMargins(10, 10, 10, 0)
        self.gridLayout_4.setSpacing(5)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.labelFlagsValue = QtWidgets.QLabel(parent=self.groupBoxProfile)
        self.labelFlagsValue.setText("")
        self.labelFlagsValue.setObjectName("labelFlagsValue")
        self.gridLayout_4.addWidget(self.labelFlagsValue, 3, 1, 1, 1)
        self.labelLevelsPlayed = QtWidgets.QLabel(parent=self.groupBoxProfile)
        self.labelLevelsPlayed.setObjectName("labelLevelsPlayed")
        self.gridLayout_4.addWidget(self.labelLevelsPlayed, 2, 0, 1, 1)
        self.labelPlayTime = QtWidgets.QLabel(parent=self.groupBoxProfile)
        self.labelPlayTime.setObjectName("labelPlayTime")
        self.gridLayout_4.addWidget(self.labelPlayTime, 1, 0, 1, 1)
        self.labelFlags = QtWidgets.QLabel(parent=self.groupBoxProfile)
        self.labelFlags.setObjectName("labelFlags")
        self.gridLayout_4.addWidget(self.labelFlags, 3, 0, 1, 1)
        self.labelProfileName = QtWidgets.QLabel(parent=self.groupBoxProfile)
        self.labelProfileName.setObjectName("labelProfileName")
        self.gridLayout_4.addWidget(self.labelProfileName, 0, 0, 1, 1)
        self.labelPlayTimeValue = QtWidgets.QLabel(parent=self.groupBoxProfile)
        self.labelPlayTimeValue.setText("")
        self.labelPlayTimeValue.setObjectName("labelPlayTimeValue")
        self.gridLayout_4.addWidget(self.labelPlayTimeValue, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_4.addItem(spacerItem1, 4, 0, 1, 2)
        self.labelProfileNameValue = QtWidgets.QLabel(parent=self.groupBoxProfile)
        self.labelProfileNameValue.setText("")
        self.labelProfileNameValue.setObjectName("labelProfileNameValue")
        self.gridLayout_4.addWidget(self.labelProfileNameValue, 0, 1, 1, 1)
        self.labelLevelsPlayedValue = QtWidgets.QLabel(parent=self.groupBoxProfile)
        self.labelLevelsPlayedValue.setText("")
        self.labelLevelsPlayedValue.setObjectName("labelLevelsPlayedValue")
        self.gridLayout_4.addWidget(self.labelLevelsPlayedValue, 2, 1, 1, 1)
        self.gridLayout_3.addWidget(self.groupBoxProfile, 0, 1, 1, 2)
        self.gridLayout_3.setColumnStretch(0, 4)
        self.gridLayout_3.setColumnStretch(1, 1)
        self.stackedWidgetProfiles.addWidget(self.pageProfileInfo)
        self.verticalLayout_5.addWidget(self.stackedWidgetProfiles)

        self.retranslateUi(ProfileTab)
        self.stackedWidgetProfiles.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(ProfileTab)

    def retranslateUi(self, ProfileTab):
        _translate = QtCore.QCoreApplication.translate
        ProfileTab.setWindowTitle(_translate("ProfileTab", "Form"))
        self.labelNoProfileFound.setText(_translate("ProfileTab", "No profile found!"))
        self.groupBoxLevels.setTitle(_translate("ProfileTab", "Levels"))
        self.groupBoxProfile.setTitle(_translate("ProfileTab", "Profile info"))
        self.labelLevelsPlayed.setText(_translate("ProfileTab", "Levels played"))
        self.labelPlayTime.setText(_translate("ProfileTab", "Play time"))
        self.labelFlags.setText(_translate("ProfileTab", "Flags"))
        self.labelProfileName.setText(_translate("ProfileTab", "Name"))