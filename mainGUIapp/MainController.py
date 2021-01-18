from typing import List
import asyncio

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap

from dataDownload.ChannelData import ChannelData
from dataDownload.VideoData import VideoData
from mainGUIapp.DownloadController import DownloadController
from mainGUIapp.videoView import VideoView
# cyclic import???
# from mainGUIapp.appView2 import Ui_MainWindow


class Controller:
    def __init__(self, window):
        self.window = window
        self.channelData = ChannelData('','','',[])
        self.downloadController = DownloadController()
        # init everything

        window.searchForChannelButton.clicked.connect(lambda: self.searchForChannel())

    def searchForChannel(self):
        providedLink = self.window.channelNameInput.toPlainText()
        self.channelData = self.downloadController.downloadChannelData(providedLink)
        self.showChannelInfo()

    def setChannelData(self, channelData: ChannelData):
        self.channelData = channelData

    def setVideosData(self, videoData: List[VideoData]):
        self.channelData.setVideosData(videoData)

    def showChannelInfo(self):

        pixmap = QPixmap(self.channelData.iconPath)
        pixmap = pixmap.scaledToHeight(64)
        self.window.channelIcon.setPixmap(pixmap)
        self.window.channelName.setText(self.channelData.channelName)
        self.window.channelSubCount.setText(self.channelData.subsCount)

        for videoData in self.channelData.videosData:
            newElement = VideoView()
            newElement.setTextUp(videoData.videoName)
            newElement.setTextDown(videoData.videoUrl)
            newElement.setVideoThumbnail('icon.png')

            myQListWidgetItem = QtWidgets.QListWidgetItem(self.window.videoElementsList)
            # Set size hint
            myQListWidgetItem.setSizeHint(newElement.sizeHint())
            # Add element to list
            self.window.videoElementsList.setItemWidget(myQListWidgetItem, newElement)
            self.window.videoElementsList.addItem(myQListWidgetItem)
