from PyQt5 import QtWidgets
from PyQt5.QtCore import QThreadPool
from PyQt5.QtGui import QPixmap

from Models.ChannelData import ChannelData
from Controller.BackgroundTasks.DownloadChannelData import DownloadChannelData
from Views.VideoElementView import VideoElementView
from Views.VideoView import VideoView


class Controller:
    def __init__(self, window):
        self.window = window
        self.channelData = ChannelData('','','',[])
        # init everything
        self.threadPool = QThreadPool()

        window.searchForChannelButton.clicked.connect(lambda: self.searchForChannel())

    def searchForChannel(self):
        providedLink = self.window.channelNameInput.toPlainText()
        print(providedLink)
        downloadTask = DownloadChannelData(self.window, self.channelData, providedLink)
        downloadTask.signals.result.connect(self.showChannelInfo)
        self.threadPool.start(downloadTask)


    def setChannelData(self, channelData: ChannelData):
        self.channelData = channelData

    def showChannelInfo(self, channelData):
        self.channelData = channelData
        pixmap = QPixmap(self.channelData.iconPath)
        pixmap = pixmap.scaledToHeight(64)
        self.window.channelIcon.setPixmap(pixmap)
        self.window.channelName.setText(self.channelData.channelName)
        self.window.channelSubCount.setText(self.channelData.subsCount)

        for videoData in self.channelData.videosData:
            newElement = VideoElementView()
            newElement.setVideoName(videoData.videoName)
            newElement.setCommentsCount("...")
            newElement.setlikeDislikeRatio("...")
            newElement.setCommentsPath("...")

            myQListWidgetItem = QtWidgets.QListWidgetItem(self.window.videoElementsList)
            # Set size hint
            myQListWidgetItem.setSizeHint(newElement.sizeHint())
            # # Add element to list
            self.window.videoElementsList.setItemWidget(myQListWidgetItem, newElement)
            self.window.videoElementsList.addItem(myQListWidgetItem)
