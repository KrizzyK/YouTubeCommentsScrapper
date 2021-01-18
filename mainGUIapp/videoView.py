from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.uic.properties import QtGui


class VideoView(QtWidgets.QWidget):
    def __init__(self):
        super(VideoView, self).__init__()

        self.mainHorizontalLayout = QtWidgets.QHBoxLayout()

        self.videoThumbnail = QtWidgets.QLabel()

        # right layout
        self.rightLayout = QtWidgets.QVBoxLayout()
        self.textUpQLabel = QtWidgets.QLabel()
        self.textDownQLabel = QtWidgets.QLabel()
        self.rightLayout.addWidget(self.textUpQLabel)
        self.rightLayout.addWidget(self.textDownQLabel)

        self.mainHorizontalLayout.addWidget(self.videoThumbnail, 0)
        self.mainHorizontalLayout.addLayout(self.rightLayout, 1)
        self.setLayout(self.mainHorizontalLayout)
        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''
                    color: rgb(0, 0, 255);
                ''')
        self.textDownQLabel.setStyleSheet('''
                    color: rgb(255, 0, 0);
                ''')

    def setTextUp(self, text):
        self.textUpQLabel.setText(text)

    def setTextDown(self, text):
        self.textDownQLabel.setText(text)

    def setVideoThumbnail(self, imagePath):
        pixmap = QPixmap(imagePath)
        pixmap = pixmap.scaledToHeight(32)
        self.videoThumbnail.setPixmap(pixmap)