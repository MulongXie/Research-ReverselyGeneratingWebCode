from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

browser = webdriver.PhantomJS()
wait = WebDriverWait(browser, 10)
browser.get('https://world.taobao.com')

browser.save_screenshot('x.png')

e = browser.find_elements_by_tag_name('body')
for s in e:
    print(s.size)