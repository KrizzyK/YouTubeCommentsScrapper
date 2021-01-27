from PyQt5 import QtWidgets, Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout


class SettingsDialog(QDialog):

    def __init__(self):
        super(SettingsDialog, self).__init__()

        self.howManyScrolls = 2
        self.timeBetweenScrolls = 3
        self.toTheEnd = False
        self.headless = False

        self.setWindowTitle("Settings")

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.layout = QVBoxLayout()
        self.layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # scroll layout
        self.scrollLayout = QtWidgets.QHBoxLayout()
        self.scrollLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        self.scrollLabel = QtWidgets.QLabel(text="Ilosc scrolli: ")
        sizePolicy.setHeightForWidth(self.scrollLabel.sizePolicy().hasHeightForWidth())
        self.scrollLabel.setSizePolicy(sizePolicy)

        self.scrollsInput = QtWidgets.QPlainTextEdit()
        sizePolicy.setHeightForWidth(self.scrollsInput.sizePolicy().hasHeightForWidth())
        self.scrollsInput.setSizePolicy(sizePolicy)
        self.scrollsInput.setMaximumSize(120, 30)
        self.scrollsInput.setPlainText("2")

        self.scrollsInput.textChanged.connect(self.scrollsChanged)

        self.scrollLayout.addWidget(self.scrollLabel)
        self.scrollLayout.addWidget(self.scrollsInput)

        # timeBetweenScrolls layout
        self.timeBetweenScrollsLayout = QtWidgets.QHBoxLayout()
        self.timeBetweenScrollsLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        self.timeLabel = QtWidgets.QLabel(text="Ilosc scrolli: ")
        sizePolicy.setHeightForWidth(self.timeLabel.sizePolicy().hasHeightForWidth())
        self.timeLabel.setSizePolicy(sizePolicy)

        self.timeBetweenScrollsInput = QtWidgets.QPlainTextEdit()
        sizePolicy.setHeightForWidth(self.timeBetweenScrollsInput.sizePolicy().hasHeightForWidth())
        self.timeBetweenScrollsInput.setSizePolicy(sizePolicy)
        self.timeBetweenScrollsInput.setMaximumSize(120,30)
        self.timeBetweenScrollsInput.setPlainText("3")
        self.timeBetweenScrollsInput.textChanged.connect(self.timeBetweenChanged)

        self.timeBetweenScrollsLayout.addWidget(self.timeLabel)
        self.timeBetweenScrollsLayout.addWidget(self.timeBetweenScrollsInput)

        # toTheEndOrNot
        self.scrollToTheEndComboBox = QtWidgets.QComboBox()
        sizePolicy.setHeightForWidth(self.scrollToTheEndComboBox.sizePolicy().hasHeightForWidth())
        self.scrollToTheEndComboBox.setSizePolicy(sizePolicy)
        self.scrollToTheEndComboBox.addItem("Przewin komentarze n razy")
        self.scrollToTheEndComboBox.addItem("Przewin komentarze do konca")
        self.scrollToTheEndComboBox.currentIndexChanged.connect(self.onIndexScrollChange)

        # headlessOrNot
        self.headlessComboBox = QtWidgets.QComboBox()
        sizePolicy.setHeightForWidth(self.headlessComboBox.sizePolicy().hasHeightForWidth())
        self.headlessComboBox.setSizePolicy(sizePolicy)
        self.headlessComboBox.addItem("Debug")
        self.headlessComboBox.addItem("Headless")
        self.headlessComboBox.currentIndexChanged.connect(self.onIndexHeadlessChange)


        self.layout.addLayout(self.scrollLayout)
        self.layout.addLayout(self.timeBetweenScrollsLayout)
        self.layout.addWidget(self.scrollToTheEndComboBox)
        self.layout.addWidget(self.headlessComboBox)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def onIndexScrollChange(self, index):
        if index == 0: self.toTheEnd = False
        else: self.toTheEnd = True

    def onIndexHeadlessChange(self, index):
        if index == 0: self.headless = False
        else: self.headless = True

    def scrollsChanged(self):
        try:
            self.howManyScrolls = int(self.scrollsInput.toPlainText())
        except Exception as e:
            pass

    def timeBetweenChanged(self):
        try:
            self.timeBetweenScrolls = int(self.timeBetweenScrollsInput.toPlainText())
        except Exception as e:
            pass

    def getSettings(self):
        return self.howManyScrolls, self.timeBetweenScrolls, self.toTheEnd, self.headless

