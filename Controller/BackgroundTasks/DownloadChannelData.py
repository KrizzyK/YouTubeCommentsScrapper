import os
import time

import wget
from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Models.ChannelData import ChannelData
from Models.VideoData import VideoData


class DownloadChannelData(QRunnable):
    def __init__(self, window, channelUrl: str, settings):
        super(DownloadChannelData, self).__init__()


        self.driver = None
        self.wait = None
        self.url = channelUrl
        self.window = window
        self.channelData = None
        self.signals = Signals()


        self.howManyScrolls = settings[0]
        self.timeBetweenScrolls = settings[1]
        self.allTheWayDown = settings[2]
        self.headless = settings[3]


    def getWebDriver(self):
        firefox_options = webdriver.FirefoxOptions()
        if self.headless:
            firefox_options.add_argument("--headless")
        return webdriver.Firefox(options=firefox_options)

    def createChannelDirectiory(self, directory):
        if not os.path.isdir(directory):
            os.makedirs(directory)

    def scrollDown(self):
        try:
            if self.allTheWayDown:
                time.sleep(6)

                get_scroll_height_command = (
                    "return (document.documentElement || document.body).scrollHeight;"
                )
                scroll_to_command = "scrollTo(0, {});"

                # Set y origin and grab the initial scroll height
                y_position = 0
                scroll_height = self.driver.execute_script(get_scroll_height_command)

                print("Opened url, scrolling to bottom of page...")
                # While the scrollbar can still scroll further down, keep scrolling
                # and asking for the scroll height to check again
                while y_position != scroll_height:
                    y_position = scroll_height
                    self.driver.execute_script(scroll_to_command.format(scroll_height))

                    # Page needs to load yet again otherwise the scroll height matches the y position
                    # and it breaks out of the loop
                    time.sleep(self.timeBetweenScrolls)
                    scroll_height = self.driver.execute_script(get_scroll_height_command)
            else:
                for _ in range(self.howManyScrolls):
                    self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
                    time.sleep(self.timeBetweenScrolls)
        except exceptions.NoSuchElementException:
            print("Error: Element title or comment section not found! ")
            return

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

        commentsPath = channelDirectoryPath + "/comments"
        videoDataList = [VideoData(videoNames, videoUrls, commentsPath, None, None)
                         for videoNames, videoUrls in zip(videoNames, videoUrls)]
        return videoDataList

    def downloadChannelData(self):
        try:
            self.driver = self.getWebDriver()
            timeout = 15
            self.wait = WebDriverWait(self.driver, timeout)
            self.driver.get(self.url)
            time.sleep(self.timeBetweenScrolls)

            channelName = self.driver.find_element_by_xpath("//*[@id='channel-name']/div/div/yt-formatted-string").text
            subscriberCount = self.driver.find_element_by_xpath("//*[@id='subscriber-count']").text
            iconUrl = self.driver.find_element_by_xpath(
                "//*[@id='channel-header-container']/yt-img-shadow/img").get_property(
                "src")

            channelDirectoryPath = "../channels/{}".format(channelName.replace(" ", "_"))
            self.createChannelDirectiory(channelDirectoryPath)

            self.scrollDown()
            videoDataList = self.getVideosData(self.driver, channelDirectoryPath)

            iconPath = channelDirectoryPath + "/channelIcon.jpg"
            if not os.path.exists(iconPath):
                wget.download(iconUrl, iconPath)

            self.channelData = ChannelData(channelName, subscriberCount, iconPath, videoDataList)
        except Exception as e:
            print(e)
        else:
            self.signals.result.emit(self.channelData)
        finally:
            if self.driver:
                self.driver.close()

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