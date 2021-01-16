# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainGUIapp\layouts\prototype.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QListWidgetItem

from mainGUIapp.videoUIelement import VideoElement


class Ui_MainWindow(object):


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 791, 561))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.mainAppLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.mainAppLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.mainAppLayout.setContentsMargins(0, 0, 0, 0)
        self.mainAppLayout.setObjectName("mainAppLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.channelNameInput = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channelNameInput.sizePolicy().hasHeightForWidth())
        self.channelNameInput.setSizePolicy(sizePolicy)
        self.channelNameInput.setMaximumSize(QtCore.QSize(16777215, 30))
        self.channelNameInput.setObjectName("channelNameInput")
        self.horizontalLayout.addWidget(self.channelNameInput)
        self.searchForChannelButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchForChannelButton.sizePolicy().hasHeightForWidth())
        self.searchForChannelButton.setSizePolicy(sizePolicy)
        self.searchForChannelButton.setObjectName("searchForChannelButton")
        self.horizontalLayout.addWidget(self.searchForChannelButton)
        self.settingsButton = QtWidgets.QToolButton(self.verticalLayoutWidget)
        self.settingsButton.setObjectName("settingsButton")
        self.horizontalLayout.addWidget(self.settingsButton)
        self.mainAppLayout.addLayout(self.horizontalLayout)

        self.videoElementsList = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.videoElementsList.setObjectName("videoElementsList")
        self.mainAppLayout.addWidget(self.videoElementsList)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # its here for a reason, couz now all the parameters in self are created
        self.searchForChannelButton.clicked.connect(lambda: self.addRandomDataToList())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.searchForChannelButton.setText(_translate("MainWindow", "Search For Channel"))
        self.settingsButton.setText(_translate("MainWindow", "Settings"))

    def addRandomDataToList(self):
        for index, name, icon in [
            ('Film1', 'URL filmu1', 'icon.png'),
            ('Film2', 'URL filmu2', 'icon.png'),
            ('Film3', 'URL filmu3', 'icon.png')]:

            newElement = VideoElement()
            newElement.setTextUp(index)
            newElement.setTextDown(name)
            newElement.setVideoThumbnail(icon)

            myQListWidgetItem = QtWidgets.QListWidgetItem(self.videoElementsList)
            # Set size hint
            myQListWidgetItem.setSizeHint(newElement.sizeHint())
            # Add element to list
            self.videoElementsList.setItemWidget(myQListWidgetItem, newElement)
            self.videoElementsList.addItem(myQListWidgetItem)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
