from functools import partial

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThreadPool
from PyQt5.QtGui import QPixmap

from Controller.BackgroundTasks.DownloadVideoComments import DownloadVideoComments
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
        downloadTask = DownloadChannelData(self.window, self.channelData, providedLink)
        downloadTask.signals.result.connect(self.showChannelInfo)
        self.threadPool.start(downloadTask)

    def downloadComments(self, videoName, url, commentsPath, videoView):
        downloadTask = DownloadVideoComments(videoName, url,
                                             commentsPath, videoView)
        downloadTask.signals.result.connect(self.analyzeVideo)
        self.threadPool.start(downloadTask)

    def analyzeVideo(self, videoData):

        pass


    def setChannelData(self, channelData: ChannelData):
        self.channelData = channelData

    def showChannelInfo(self, channelData):
        try:
            self.channelData = channelData
            pixmap = QPixmap(self.channelData.iconPath)
            pixmap = pixmap.scaledToHeight(64)
            self.window.channelIcon.setPixmap(pixmap)
            self.window.channelName.setText(self.channelData.channelName)
            self.window.channelSubCount.setText(self.channelData.subsCount)
            print(self.channelData.__str__())
            for videoData in self.channelData.videosData:
                newElement = VideoElementView()
                newElement.setVideoName(videoData.videoName)
                # newElement.setCommentsCount(videoData.commentsCount)
                # newElement.setlikeDislikeRatio(videoData.likeDislikeRatio)

                myQListWidgetItem = QtWidgets.QListWidgetItem(self.window.videoElementsList)
                # Set size hint
                myQListWidgetItem.setSizeHint(newElement.sizeHint())
                # # Add element to list
                self.window.videoElementsList.setItemWidget(myQListWidgetItem, newElement)
                self.window.videoElementsList.addItem(myQListWidgetItem)
                newElement.analyzeButton.clicked.connect(
                    partial(self.downloadComments,videoData.videoName,
                            videoData.videoUrl, videoData.commentsPath, newElement))
                #  https://stackoverflow.com/questions/6784084/how-to-pass-arguments-to-functions-by-the-click-of-button-in-pyqt/42945033
        except Exception as e:
            print(e)
        else:
            pass