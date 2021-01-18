import os
import time

import wget
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal
from PyQt5.QtGui import QPixmap
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from dataDownload.ChannelData import ChannelData
from dataDownload.VideoData import VideoData
from mainGUIapp.appView import Ui_MainWindow
from mainGUIapp.videoView import VideoView


class DownloadChannelData(QRunnable):
    def __init__(self, window: Ui_MainWindow, channelData: ChannelData, channelUrl: str):
        super(DownloadChannelData, self).__init__()

        self.url = channelUrl
        self.window = window
        self.channelData = channelData
        self.signals = Signals()


    def getWebDriver(self):
        firefox_options = webdriver.FirefoxOptions()
        # firefox_options.add_argument("--headless")
        return webdriver.Firefox(options=firefox_options)

    def createChannelDirectiory(self, directory):
        if not os.path.isdir(directory):
            os.makedirs(directory)

    # assuming the driver opened the yt videos page
    def getVideosData(self, driver, channelDirectoryPath: str):
        videoUrls = [
            videoURL.get_attribute("href") + "\n"
            for videoURL in driver.find_elements_by_xpath("//*[@id='video-title']")
        ]
        videoNames = [
            videoName.get_property("title")
            for videoName in driver.find_elements_by_xpath("//*[@id='video-title']")
        ]

        with open(channelDirectoryPath + "/videoUrls.txt", "a") as file:
            file.writelines(videoUrls)

        videoDataList = [VideoData(videoNames, videoUrls)
                         for videoNames, videoUrls in zip(videoNames, videoUrls)]
        return videoDataList

    def downloadChannelData(self):
        try:
            driver = self.getWebDriver()
            timeout = 15
            wait = WebDriverWait(driver, timeout)
            driver.get(self.url)
            time.sleep(3)

            channelName = driver.find_element_by_xpath("//*[@id='channel-name']/div/div/yt-formatted-string").text
            subscriberCount = driver.find_element_by_xpath("//*[@id='subscriber-count']").text
            iconUrl = driver.find_element_by_xpath(
                "//*[@id='channel-header-container']/yt-img-shadow/img").get_property(
                "src")

            channelDirectoryPath = "channels/{}".format(channelName.replace(" ", "_"))
            self.createChannelDirectiory(channelDirectoryPath)

            videoDataList = self.getVideosData(driver, channelDirectoryPath)

            iconPath = channelDirectoryPath + "/channelIcon.jpg"
            if not os.path.exists(iconPath):
                wget.download(iconUrl, iconPath)

            self.channelData = ChannelData(channelName, subscriberCount, iconPath, videoDataList)
            print(self.channelData)
        except Exception as e:
            print(e)
        else:
            self.signals.result.emit(self.channelData)
        finally:
            if driver:
                driver.close()

    @pyqtSlot()
    def run(self):
        print("Download start")
        self.downloadChannelData()
        print("Download complete")


class Signals(QObject):
    '''
    Used signals are:
    result - object data returned from processing, anything
    progress - int indicating % progress
    src: https://www.learnpyqt.com/tutorials/multithreading-pyqt-applications-qthreadpool/
    '''
    result = pyqtSignal(ChannelData)
    progress = pyqtSignal(int)