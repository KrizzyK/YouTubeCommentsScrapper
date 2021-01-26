from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSizePolicy


class VideoElementView(QWidget):
    def __init__(self):
        super(VideoElementView, self).__init__()

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        font = QtGui.QFont()
        font.setPointSize(12)
        self.title = QtWidgets.QLabel(text="Video Title")
        self.title.setFont(font)
        sizePolicy.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(sizePolicy)

        self.analyzeButton = QtWidgets.QPushButton(text="Analyze")
        # self.analyzeButton.setMaximumSize(60, 300);
        sizePolicy.setHeightForWidth(self.analyzeButton.sizePolicy().hasHeightForWidth())
        self.analyzeButton.setSizePolicy(sizePolicy)

        self.commentsCount = QtWidgets.QLabel(text="CommCount")
        sizePolicy.setHeightForWidth(self.commentsCount.sizePolicy().hasHeightForWidth())
        self.commentsCount.setSizePolicy(sizePolicy)

        self.likeDislikeRatio = QtWidgets.QLabel(text="Like/Dislike")
        sizePolicy.setHeightForWidth(self.likeDislikeRatio.sizePolicy().hasHeightForWidth())
        self.likeDislikeRatio.setSizePolicy(sizePolicy)

        self.leftSubLayout = QtWidgets.QHBoxLayout()
        self.leftSubLayout.addWidget(self.commentsCount, Qt.AlignLeft)
        self.leftSubLayout.addWidget(self.likeDislikeRatio, Qt.AlignLeft)
        self.leftSubLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        self.leftLayout = QtWidgets.QVBoxLayout()
        self.leftLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.leftLayout.addWidget(self.title, Qt.AlignLeft)
        self.leftLayout.addLayout(self.leftSubLayout, Qt.AlignLeft)
        self.leftLayout.addWidget(self.analyzeButton, Qt.AlignLeft)


        self.line = QtWidgets.QFrame()
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)

        # right layout
        self.rightLayout = QtWidgets.QVBoxLayout()

        self.mainLayout.addLayout(self.leftLayout, Qt.AlignLeft)
        self.mainLayout.addWidget(self.line, Qt.AlignLeft)
        self.mainLayout.addLayout(self.rightLayout, Qt.AlignLeft)

        self.setLayout(self.mainLayout)

    def setVideoName(self, text: str):
        if len(text) > 25:
            self.title.setText(text[0:25])
        else:

            self.title.setText(text.ljust(25, ' '))

    def setCommentsCount(self, text):
        self.commentsCount.setText(text)

    def setLikeDislikeRatio(self, text):
        self.likeDislikeRatio.setText(text)
