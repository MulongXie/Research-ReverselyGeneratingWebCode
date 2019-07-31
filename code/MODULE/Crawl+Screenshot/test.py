import os
from selenium import webdriver

driver = webdriver.PhantomJS(executable_path=os.path.join('D://webdriver', 'phantomjs.exe'))
driver.implicitly_wait(10)
driver.get_window_size('http://www.google.com')
