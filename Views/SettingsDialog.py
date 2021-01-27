from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout


class SettingsDialog(QDialog):

    def __init__(self):
        super(SettingsDialog, self).__init__()

        self.toTheEnd = False
        self.timeBetweenScrolls = 3
        self.howManyScrolls = 2

        self.setWindowTitle("Settings")

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # scroll layout
        self.scrollLayout = QtWidgets.QHBoxLayout()
        self.scrollLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.scrollName = QtWidgets.QLabel(text= "Ilosc scrolli: ")
        sizePolicy.setHeightForWidth(self.scrollName.sizePolicy().hasHeightForWidth())
        self.scrollName.setSizePolicy(sizePolicy)

        self.scrolls = QtWidgets.QPlainTextEdit()
        sizePolicy.setHeightForWidth(self.scrolls.sizePolicy().hasHeightForWidth())
        self.scrolls.setSizePolicy(sizePolicy)
        self.scrolls.setPlainText("2")

        self.scrolls.textChanged.connect( self.scrollsChanged )

        self.scrollLayout.addWidget(self.scrollName)
        self.scrollLayout.addWidget(self.scrolls)

        # timeBetweenScrolls layout
        self.timeBetweenLayout = QtWidgets.QHBoxLayout()
        self.timeBetweenLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.timeLabel = QtWidgets.QLabel(text="Ilosc scrolli: ")
        sizePolicy.setHeightForWidth(self.timeLabel.sizePolicy().hasHeightForWidth())
        self.timeLabel.setSizePolicy(sizePolicy)

        self.timeBetween = QtWidgets.QPlainTextEdit()
        sizePolicy.setHeightForWidth(self.timeBetween.sizePolicy().hasHeightForWidth())
        self.timeBetween.setSizePolicy(sizePolicy)
        self.timeBetween.setPlainText("3")
        self.timeBetween.textChanged.connect( self.timeBetweenChanged )

        self.timeBetweenLayout.addWidget(self.timeLabel)
        self.timeBetweenLayout.addWidget(self.timeBetween)

        # toTheEndOrNot
        self.comboBox = QtWidgets.QComboBox()
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.addItem("Przewin komentarze n razy")
        self.comboBox.addItem("Przewin komentarze do konca")
        # self.comboBox.currentIndexChanged.connect(self.selectionchange)
        # self.comboBox.activated[str].connect(self.onActivated)
        self.comboBox.currentIndexChanged.connect(self.onIndexChange)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.scrollLayout)
        self.layout.addLayout(self.timeBetweenLayout)
        self.layout.addWidget(self.comboBox)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def onIndexChange(self, index):
        if index == 0: self.toTheEnd = False
        else: self.toTheEnd = True

    def scrollsChanged(self):
        try:
            self.howManyScrolls = int(self.scrolls.toPlainText())
        except Exception as e:
            pass

    def timeBetweenChanged(self):
        try:
            self.timeBetweenScrolls = int(self.timeBetween.toPlainText())
        except Exception as e:
            pass

    def getSettings(self):
        return self.howManyScrolls, self.timeBetweenScrolls, self.toTheEnd

