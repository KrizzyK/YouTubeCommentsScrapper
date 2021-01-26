import os
from typing import List

from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from Models.VideoData import VideoData


class DownloadVideoComments(QRunnable):
    def __init__(self, videoName, videoUrl, commentsPath, videoElementView):
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

    def getWebDriver(self):
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--headless")
        return webdriver.Firefox(options=firefox_options)

    def scrollDown(self, allTheWayDown: bool = False, howManyScrolls: int = 20) -> None:
        try:
            comment_section = self.driver.find_element_by_xpath('//*[@id="comments"]')
            time.sleep(6)
            self.driver.execute_script("arguments[0].scrollIntoView();", comment_section)
        except exceptions.NoSuchElementException:
            print("Error: Element title or comment section not found! ")
            return

        if allTheWayDown:
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
                time.sleep(2)
                scroll_height = self.driver.execute_script(get_scroll_height_command)
        else:
            for _ in range(howManyScrolls):
                self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
                time.sleep(2)

    def getComments(self):
        self.commentsCount = self.driver.find_element_by_xpath\
        ("/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/h2/yt-formatted-string" ).text
        self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content")))
        self.comments = [comment_element.text
                         for comment_element in self.driver.find_elements_by_xpath("//*[@id='content-text']")]

    def saveComments(self, comments):
        if not os.path.isdir(self.commentsPath):
            os.makedirs(self.commentsPath)

        with open(self.commentsPath +"/"+ self.videoName.replace(" ", "_") + ".txt", 'w', encoding="utf-8") as f:
            for item in comments:
                f.write("%s\n" % item)

    def downloadVideoData(self):
        try:
            self.driver = self.getWebDriver()
            timeout = 15
            self.wait = WebDriverWait(self.driver, timeout)
            self.driver.get(self.videoUrl)
            self.scrollDown(False,3)
            self.getComments()
            self.saveComments(self.comments)
            self.videoData = VideoData(self.videoName, self.videoUrl,self.commentsPath,
                                       self.videoView, self.comments, self.commentsCount)
        except Exception as e:
            print(e)
        else:
            self.signals.result.emit(self.videoData)
        finally:
            if self.driver:
                self.driver.close()

    @pyqtSlot()
    def run(self):
        print("Download start")
        self.downloadVideoData()
        print("Download complete")


class Signals(QObject):
    '''
    Used signals are:
    result - object data returned from processing, anything
    progress - int indicating % progress
    src: https://www.learnpyqt.com/tutorials/multithreading-pyqt-applications-qthreadpool/
    '''
    result = pyqtSignal(VideoData)
    progress = pyqtSignal(int)
