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
        self.mainLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        # left layout
        font = QtGui.QFont()
        font.setPointSize(12)
        self.title = QtWidgets.QLabel(text="Video Title")
        self.title.setFont(font)
        self.title.setMinimumSize(300, 0)
        sizePolicy.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(sizePolicy)

        self.analyzeButton = QtWidgets.QPushButton(text="Analizuj")
        # self.analyzeButton.setMaximumSize(60, 300);
        sizePolicy.setHeightForWidth(self.analyzeButton.sizePolicy().hasHeightForWidth())
        self.analyzeButton.setSizePolicy(sizePolicy)


        self.leftLayout = QtWidgets.QVBoxLayout()
        self.leftLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.leftLayout.addWidget(self.title, Qt.AlignLeft)
        self.leftLayout.addWidget(self.analyzeButton, Qt.AlignLeft)

        # line
        self.line = QtWidgets.QFrame()
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)

        # right layout
        self.amountOfDownloadedComments = QtWidgets.QLabel(text="Pobrane komentarze: ")
        sizePolicy.setHeightForWidth(self.amountOfDownloadedComments.sizePolicy().hasHeightForWidth())
        self.amountOfDownloadedComments.setSizePolicy(sizePolicy)

        self.amountOfNeutralComments = QtWidgets.QLabel(text="Neutralne komentarze: ")
        sizePolicy.setHeightForWidth(self.amountOfNeutralComments.sizePolicy().hasHeightForWidth())
        self.amountOfNeutralComments.setSizePolicy(sizePolicy)

        self.amountOfPositiveComments = QtWidgets.QLabel(text="Pozytywne komentarze: ")
        sizePolicy.setHeightForWidth(self.amountOfPositiveComments.sizePolicy().hasHeightForWidth())
        self.amountOfPositiveComments.setSizePolicy(sizePolicy)

        self.amountOfNegativeComments = QtWidgets.QLabel(text="Negatywne komentarze: ")
        sizePolicy.setHeightForWidth(self.amountOfNegativeComments.sizePolicy().hasHeightForWidth())
        self.amountOfNegativeComments.setSizePolicy(sizePolicy)


        self.rightLayout = QtWidgets.QVBoxLayout()
        self.rightLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.rightLayout.addWidget(self.amountOfDownloadedComments, Qt.AlignLeft)
        self.rightLayout.addWidget(self.amountOfNeutralComments, Qt.AlignLeft)
        self.rightLayout.addWidget(self.amountOfPositiveComments, Qt.AlignLeft)
        self.rightLayout.addWidget(self.amountOfNegativeComments, Qt.AlignLeft)


        self.mainLayout.addLayout(self.leftLayout, Qt.AlignLeft)
        self.mainLayout.addWidget(self.line, Qt.AlignLeft)
        self.mainLayout.addLayout(self.rightLayout, Qt.AlignLeft)

        self.setLayout(self.mainLayout)

    def setVideoName(self, text: str):
        if len(text) > 25:
            self.title.setText(text[0:25] + "...")
        else:
            self.title.setText(text.ljust(28, ' ') )


    def setAmountOfDownloadedComments(self, text):
        self.amountOfDownloadedComments.setText("Pobrane komentarze: " +str(text))

    def setAmountOfNeutralComments(self, text):
        self.amountOfNeutralComments.setText("Neutralne komentarze: " + str(text))

    def setAmountOfNegativeComments(self, text):
        self.amountOfNegativeComments.setText("Negatywne komentarze: " + str(text))

    def setAmountOfPositiveComments(self, text):
        self.amountOfPositiveComments.setText("Pozytywne komentarze: " + str(text))