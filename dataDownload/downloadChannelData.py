import os
import time
import wget

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from dataDownload.ChannelData import ChannelData
from dataDownload.VideoData import VideoData


def getWebDriver():
    firefox_options = webdriver.FirefoxOptions()
    # firefox_options.add_argument("--headless")
    return webdriver.Firefox(options=firefox_options)


def createChannelDirectiory(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)


# assuming the driver opened the yt videos page
def getVideosData(driver, channelDirectoryPath):
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


# assuming the driver opened the yt videos page
def downloadChannelData(driver):
    channelName = driver.find_element_by_xpath("//*[@id='channel-name']/div/div/yt-formatted-string").text
    subscriberCount = driver.find_element_by_xpath("//*[@id='subscriber-count']").text
    iconUrl = driver.find_element_by_xpath("//*[@id='channel-header-container']/yt-img-shadow/img").get_property("src")

    channelDirectoryPath = "channels/{}".format(channelName.replace(" ", "_"))
    createChannelDirectiory(channelDirectoryPath)

    videoDataList = getVideosData(driver, channelDirectoryPath)

    iconPath = channelDirectoryPath + "/channelIcon.jpg"
    if not os.path.exists(iconPath):
        wget.download(iconUrl, iconPath)

    return ChannelData(channelName, subscriberCount, iconPath, videoDataList)


if __name__ == '__main__':
    driver = getWebDriver()

    timeout = 15
    wait = WebDriverWait(driver, timeout)
    try:
        driver.get("https://www.youtube.com/c/bmpromotion/videos")  # yt channel videos page URL
        channelData = downloadChannelData(driver)
        print(channelData)
        time.sleep(3)

    except Exception as e:
        print(e)
    finally:
        if driver:
            driver.close()
