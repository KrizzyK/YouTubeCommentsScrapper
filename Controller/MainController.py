from functools import partial

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThreadPool
from PyQt5.QtGui import QPixmap

from Controller.BackgroundTasks.DownloadVideoComments import DownloadVideoComments
from Models.ChannelData import ChannelData
from Controller.BackgroundTasks.DownloadChannelData import DownloadChannelData
from Views.VideoElementView import VideoElementView


class Controller:
    def __init__(self, window):
        self.window = window
        self.channelData = ChannelData('', '', '', [])
        self.threadPool = QThreadPool()
        self.wordsRatingDict = None
        window.searchForChannelButton.clicked.connect(lambda: self.downloadChannelInformation())

    def downloadChannelInformation(self):
        providedLink = self.window.channelNameInput.toPlainText()
        downloadTask = DownloadChannelData(self.window, providedLink)
        downloadTask.signals.result.connect(self.showChannelInfo)
        self.threadPool.start(downloadTask)

    def downloadComments(self, videoName, url, commentsPath, videoView):
        downloadTask = DownloadVideoComments(videoName, url,
                                             commentsPath, videoView)
        downloadTask.signals.result.connect(self.analyzeVideo)
        self.threadPool.start(downloadTask)


    def getDictOfWordsRating(self):
        # there was "lambda (k,v): (k,int(v)) "
        # lambda (x, y): x + y will be translated into: lambda x_y: x_y[0] + x_y[1]
        if self.wordsRatingDict is None:
            self.wordsRatingDict = dict(map(lambda k_v: (k_v[0], int(k_v[1])),
                                            [line.split('\t') for line in open(
                                                "../SentimentAnalysis/AFINN-111.txt")]))

    def analyzeVideo(self, videoData):
        try:
            self.getDictOfWordsRating()
            videoData.videoView.setTextBelowTitle(videoData.commentsCount)

            listOfRatings = [sum(map(lambda word: self.wordsRatingDict.get(word, 0), comment.lower().split()))
                             for comment in videoData.comments]
            positive = negative = neutral = 0
            for rating in listOfRatings:
                if rating == 0: neutral+=1
                elif rating > 0: positive+=1
                else: negative+=1
            videoData.videoView.setAmountOfNegativeComments(negative)
            videoData.videoView.setAmountOfPositiveComments(positive)
            videoData.videoView.setAmountOfNeutralComments(neutral)
            videoData.videoView.setAmountOfDownloadedComments(len(listOfRatings))


        except Exception as e:
            print(e)

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
            for videoData in self.channelData.videosData:
                newElement = VideoElementView()
                newElement.setVideoName(videoData.videoName)
                newElement.setTextBelowTitle("???")

                myQListWidgetItem = QtWidgets.QListWidgetItem(self.window.videoElementsList)
                myQListWidgetItem.setSizeHint(newElement.sizeHint())
                self.window.videoElementsList.setItemWidget(myQListWidgetItem, newElement)
                self.window.videoElementsList.addItem(myQListWidgetItem)
                newElement.analyzeButton.clicked.connect(
                    partial(self.downloadComments, videoData.videoName,
                            videoData.videoUrl, videoData.commentsPath, newElement))
                #  https://stackoverflow.com/questions/6784084/how-to-pass-arguments-to-functions-by-the-click-of-button-in-pyqt/42945033
        except Exception as e:
            print(e)
        else:
            pass
