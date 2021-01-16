from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def getWebDriver():
    firefox_options = webdriver.FirefoxOptions()
    # firefox_options.add_argument("--headless")
    return webdriver.Firefox(options=firefox_options)


def scrollDown(howManyScrolls: int) -> None:
    time.sleep(2)
    try:
        title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
        comment_section = driver.find_element_by_xpath('//*[@id="comments"]')
    except exceptions.NoSuchElementException:
        print("Error: Element title or comment section not found! ")
        return

    driver.execute_script("arguments[0].scrollIntoView();", comment_section)

    i = 1
    for item in range(howManyScrolls):
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
        print("scroll {}".format(i))
        i += 1
        time.sleep(1.5)

    # time.sleep(5)
    #
    # get_scroll_height_command = (
    #     "return (document.documentElement || document.body).scrollHeight;"
    # )
    # scroll_to_command = "scrollTo(0, {});"
    #
    # # Set y origin and grab the initial scroll height
    # y_position = 0
    # scroll_height = driver.execute_script(get_scroll_height_command)
    #
    # print("Opened url, scrolling to bottom of page...")
    # # While the scrollbar can still scroll further down, keep scrolling
    # # and asking for the scroll height to check again
    # while y_position != scroll_height:
    #     y_position = scroll_height
    #     driver.execute_script(scroll_to_command.format(scroll_height))
    #
    #     # Page needs to load yet again otherwise the scroll height matches the y position
    #     # and it breaks out of the loop
    #     time.sleep(4)
    #     scroll_height = driver.execute_script(get_scroll_height_command)


def getComments():
    data = []
    # for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content"))):
    #     data.append(comment.text)
        # print(comment.text)

    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content")))
    comments_list = [comment_element.text
                     for comment_element in driver.find_elements_by_xpath("//*[@id='content-text']")]

    return comments_list


if __name__ == '__main__':
    driver = getWebDriver()

    timeout = 15
    wait = WebDriverWait(driver, timeout)
    # driver.get("https://www.youtube.com/watch?v=Qj6xHRYFKek") # ~ 30 comments ?
    driver.get("https://www.youtube.com/watch?v=xgfa5UlZAL8") # a lot of comments
    scrollDown(12)
    data = getComments()
    print(len(data))
    print(data)
