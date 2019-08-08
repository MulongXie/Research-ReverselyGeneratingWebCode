from selenium import webdriver

driver = webdriver.PhantomJS('D:/webdriver/phantomjs.exe')
driver.set_page_load_timeout(5)

try:
    driver.get('https://blog.csdn.net/supramolecular/article/details/82386564')
except TimeoutError:
    driver.execute_script('window.stop ? window.stop() : document.execCommand("Stop");')