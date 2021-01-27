# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainGUIapp\layouts\prototype.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from Controller.MainController import Controller
import qtmodern.styles
import qtmodern.windows

from Views.SettingsDialog import SettingsDialog
from Views.VideoView import VideoView





class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("YouTubeScrapper")
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
        self.searchLayout = QtWidgets.QHBoxLayout()
        self.searchLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.searchLayout.setObjectName("searchLayout")
        self.channelNameInput = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channelNameInput.sizePolicy().hasHeightForWidth())
        self.channelNameInput.setSizePolicy(sizePolicy)
        self.channelNameInput.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.channelNameInput.setFont(font)
        self.channelNameInput.setPlainText("https://www.youtube.com/c/bmpromotion/videos")
        self.channelNameInput.setObjectName("channelNameInput")
        self.searchLayout.addWidget(self.channelNameInput)

        self.searchForChannelButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.searchForChannelButton.setObjectName("searchForChannelButton")
        self.searchLayout.addWidget(self.searchForChannelButton)

        self.settingsButton = QtWidgets.QToolButton(self.verticalLayoutWidget)
        self.settingsButton.setObjectName("settingsButton")
        self.searchLayout.addWidget(self.settingsButton)
        self.mainAppLayout.addLayout(self.searchLayout)
        self.channelInfoLayout = QtWidgets.QHBoxLayout()
        self.channelInfoLayout.setObjectName("channelInfoLayout")
        self.channelIcon = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.channelIcon.setMinimumSize(QtCore.QSize(64, 64))
        self.channelIcon.setMaximumSize(QtCore.QSize(64, 64))
        self.channelIcon.setText("")
        self.channelIcon.setObjectName("channelIcon")
        self.channelInfoLayout.addWidget(self.channelIcon)
        self.channelInfoSubLayout = QtWidgets.QVBoxLayout()
        self.channelInfoSubLayout.setObjectName("channelInfoSubLayout")
        self.channelName = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.channelName.setFont(font)
        self.channelName.setObjectName("channelName")
        self.channelInfoSubLayout.addWidget(self.channelName)
        self.channelSubCount = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.channelSubCount.setObjectName("channelSubCount")
        self.channelInfoSubLayout.addWidget(self.channelSubCount)
        self.channelInfoLayout.addLayout(self.channelInfoSubLayout)
        self.mainAppLayout.addLayout(self.channelInfoLayout)
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

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "YouTubeCommentsScrapper"))
        self.searchForChannelButton.setText(_translate("MainWindow", "Szukaj kanalu"))
        self.settingsButton.setText(_translate("MainWindow", "Ustawienia"))
        self.channelName.setText(_translate("MainWindow", "Nazwa kanalu"))
        self.channelSubCount.setText(_translate("MainWindow", "Ilosc subskrypcji"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    qtmodern.styles.dark(app)
    mw = qtmodern.windows.ModernWindow(MainWindow)
    mw.show()

    controller = Controller(ui)
    sys.exit(app.exec_())

