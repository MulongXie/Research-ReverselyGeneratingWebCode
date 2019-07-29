from selenium import webdriver
import time


driver = webdriver.PhantomJS('D:\git_file\github\doing\Research-ReverselyGeneratingWebCode\code\webdriver\phantomjs')
driver.get('https://youtube.com')

s = driver.find_elements_by_tag_name('body')

for b in s:
    print(b.size)
    print(driver.get_window_size())