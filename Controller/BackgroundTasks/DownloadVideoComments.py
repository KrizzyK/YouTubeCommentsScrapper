import os
from typing import List

from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from Models.VideoData import VideoData


class DownloadVideoComments(QRunnable):
    def __init__(self, videoName, videoUrl, commentsPath, videoElementView, settings):
        super(DownloadVideoComments, self).__init__()
        self.driver = None
        self.wait = None
        self.signals = Signals()

        self.videoName = videoName
        self.videoUrl = videoUrl
        self.videoView = videoElementView
        self.commentsPath = commentsPath
        self.commentsCount = "0"
        self.comments = []
        self.videoData = None

        self.allTheWayDown = settings[2]
        self.howManyScrolls = settings[0]
        self.timeBetweenScrolls = settings[1]

    def getWebDriver(self):
        firefox_options = webdriver.FirefoxOptions()
        # firefox_options.add_argument("--headless")
        return webdriver.Firefox(options=firefox_options)

    def scrollDown(self) -> None:
        try:
            if self.allTheWayDown:
                comment_section = self.driver.find_element_by_xpath('//*[@id="comments"]')
                time.sleep(6)
                self.driver.execute_script("arguments[0].scrollIntoView();", comment_section)

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

    def getComments(self):
        # self.commentsCount = self.driver.find_element_by_xpath\
        # ("/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/h2/yt-formatted-string" ).text
        self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content")))
        self.comments = [comment_element.text
                         for comment_element in self.driver.find_elements_by_xpath("//*[@id='content-text']")]

    def saveComments(self, comments):
        path = self.commentsPath +"/"+ self.videoName.replace(" ", "_")
        if not os.path.isdir(path):
            os.makedirs(path)

        with open(path + "/comments.txt", 'w', encoding="utf-8") as f:
            for item in comments:
                f.write("%s\n" % item)

    def downloadVideoData(self):
        try:
            print(self.howManyScrolls, self.timeBetweenScrolls, self.allTheWayDown)
            self.driver = self.getWebDriver()
            timeout = 15
            self.wait = WebDriverWait(self.driver, timeout)
            self.driver.get(self.videoUrl)
            self.scrollDown()
            self.getComments()
            self.saveComments(self.comments)
            self.videoData = VideoData(self.videoName, self.videoUrl,self.commentsPath,
                                       self.videoView, self.comments, self.commentsCount)
        except Exception as e:
            print(e)
            self.signals.result.emit(None)
        else:
            self.signals.result.emit(self.videoData)
        finally:
            if self.driver:
                self.driver.close()

    @pyqtSlot()
    def run(self):
        print("Download comments from " + self.videoName + " started")
        self.downloadVideoData()
        print("Download comments from " + self.videoName + " complete")


class Signals(QObject):
    '''
    Used signals are:
    result - object data returned from processing, anything
    progress - int indicating % progress
    src: https://www.learnpyqt.com/tutorials/multithreading-pyqt-applications-qthreadpool/
    '''
    result = pyqtSignal(VideoData)
    progress = pyqtSignal(int)
