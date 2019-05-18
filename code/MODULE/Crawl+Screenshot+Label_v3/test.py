import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = 'https://www.ebay.com/'
PIC_PATH = os.path.join(os.path.expanduser('~'), 'Pictures/python/screenshot')
PIC_NAME = 'screenshot.png'


def screenshot_web(url=URL, path=PIC_PATH, name=PIC_NAME):
    '''capture the whole web page
    :param url: the website url
    :type url: str
    :param path: the path for saving picture
    :type str
    :param name: the name of picture
    :type name: str
    '''
    if not os.path.exists(path):
        os.makedirs(path)
    browser = webdriver.PhantomJS()

    browser.get(url)
    logging.debug('request completed')

    pic_path = 'x.png'
    print(pic_path)
    if browser.save_screenshot(pic_path):
        print('Done!')
    else:
        print('Failed!')


if __name__ == '__main__':
    screenshot_web()