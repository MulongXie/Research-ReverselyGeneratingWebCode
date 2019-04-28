from selenium import webdriver
import time
import os.path
import multiprocessing as mp
from selenium.webdriver.chrome.options import Options


def webshot(link):

    options = webdriver.ChromeOptions()
    # ****** critical ******
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(link)
        scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(scroll_width, scroll_height)
        driver.save_screenshot('aaa' + ".png")
        print("Process get one pic !!!")
    except Exception as e:
        print('aaa', e)


if __name__ == '__main__':
    webshot("https://cecs.anu.edu.au/")