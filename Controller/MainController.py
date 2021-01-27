import os
from functools import partial

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThreadPool
from PyQt5.QtGui import QPixmap

from Controller.BackgroundTasks.DownloadVideoComments import DownloadVideoComments
from Models.ChannelData import ChannelData
from Controller.BackgroundTasks.DownloadChannelData import DownloadChannelData
from Views.SettingsDialog import SettingsDialog
from Views.VideoElementView import VideoElementView


class Controller:
    def __init__(self, window):
        self.window = window
        self.channelData = ChannelData('', '', '', [])
        self.threadPool = QThreadPool()
        self.wordsRatingDict = None
        self.settings = (2, 3, False)
        window.searchForChannelButton.clicked.connect(lambda: self.downloadChannelInformation())
        window.settingsButton.clicked.connect(lambda: self.showSettingsDialog())

    def showSettingsDialog(self):
        dlg = SettingsDialog()
        if dlg.exec_():
            self.settings = dlg.getSettings()
        else:
            print("Cancel!")

    def downloadChannelInformation(self):
        providedLink = self.window.channelNameInput.toPlainText()
        downloadTask = DownloadChannelData(self.window, providedLink, self.settings)
        downloadTask.signals.result.connect(self.showChannelInfo)
        self.threadPool.start(downloadTask)

    def downloadComments(self, videoName, url, commentsPath, videoView):
        downloadTask = DownloadVideoComments(videoName, url,
                                             commentsPath, videoView, self.settings)
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

            listOfRatings = [sum(map(lambda word: self.wordsRatingDict.get(word, 0), comment.lower().split()))
                             for comment in videoData.comments]
            positive = neutral = 0
            for rating in listOfRatings:
                if rating == 0:
                    neutral += 1
                elif rating > 0:
                    positive += 1

            # on gui
            videoData.videoView.setAmountOfNegativeComments(len(listOfRatings) - positive)
            videoData.videoView.setAmountOfPositiveComments(positive)
            videoData.videoView.setAmountOfNeutralComments(neutral)
            videoData.videoView.setAmountOfDownloadedComments(len(listOfRatings))
            # to file
            path = videoData.commentsPath + "/" + videoData.videoName.replace(" ", "_")
            self.createDirectory(path)
            with open(path + "/stats.txt", 'w', encoding="utf-8") as f:
                f.write("Pobrane komentarze: " + str(len(listOfRatings)))
                f.write("Neutralne komentarze: " + str(neutral))
                f.write("Pozytywne komentarze: " + str(positive))
                f.write("Negatywne komentarze: " + str(len(listOfRatings) - positive) )
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

                myQListWidgetItem = QtWidgets.QListWidgetItem(self.window.videoElementsList)
                myQListWidgetItem.setSizeHint(newElement.sizeHint())

                list = self.window.videoElementsList
                list.setItemWidget(myQListWidgetItem, newElement)
                list.insertItem(list.count(), myQListWidgetItem)
                newElement.analyzeButton.clicked.connect(
                    partial(self.downloadComments, videoData.videoName,
                            videoData.videoUrl, videoData.commentsPath, newElement))
                #  https://stackoverflow.com/questions/6784084/how-to-pass-arguments-to-functions-by-the-click-of-button-in-pyqt/42945033
        except Exception as e:
            print(e)
        else:
            pass

    def createDirectory(self, directory):
        if not os.path.isdir(directory):
            os.makedirs(directory)

