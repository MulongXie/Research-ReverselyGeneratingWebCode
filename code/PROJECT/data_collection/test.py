import os
from selenium import webdriver

driver = webdriver.PhantomJS(executable_path=os.path.join('D://webdriver', 'phantomjs.exe'))
driver.set_page_load_timeout(10)

try:
    driver.get('http://clickondetroit.com ')
except:
    print('time out')
finally:
    print('aaa')