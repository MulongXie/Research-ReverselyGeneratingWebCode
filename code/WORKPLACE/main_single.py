import pandas as pd
from selenium import webdriver
import cv2
from os.path import join as pjoin
from func_timeout import func_set_timeout, FunctionTimedOut
import time
import os

def draw(label, pic):
    def select_color(item):
        color = (0, 0, 0)
        if item == 'div':
            color = (0, 0, 200)
        elif item == 'input':
            color = (255, 0, 0)
        elif item == 'button':
            color = (180, 0, 0)
        elif item == 'h1':
            color = (0, 255, 0)
        elif item == 'h2':
            color = (0, 180, 0)
        elif item == 'p':
            color = (0, 100, 0)
        elif item == 'a':
            color = (200, 100,)
        elif item == 'img':
            color = (0, 100, 255)
        return color

    count = {}
    for i in range(0, len(label)):
        item = label.iloc[i]
        top_left = (int(item.bx), int(item.by))
        botom_right = (int(item.bx + item.bw), int(item.by + item.bh))
        element = item.element
        color = select_color(item.element)
        if element in count:
            count[element] += 1
        else:
            count[element] = 1
        pic = cv2.rectangle(pic, top_left, botom_right, color, 1)
        cv2.putText(pic, element + str(count[element]), top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)


def fetch_element(ele_name, ele_all):
    elements_dom = driver.find_elements_by_xpath('//' + ele_name)
    for e in elements_dom:
        elements = {'element':ele_name,
                    'bx': e.location['x'],
                    'by': e.location['y'],
                    'bw': e.size['width'],
                    'bh': e.size['height']}
        ele_all = ele_all.append(elements, True)
    return ele_all


@func_set_timeout(60)
def crawl(url):
    try:
        driver.get(url)
    except FunctionTimedOut:
        return None, None


if __name__ == '__main__':
    # set output
    url = 'http://ynhhs.org'
    index = 1
    path_org = pjoin('data', 'org', str(index) + '.png')
    path_drawn = pjoin('data', 'drawn', str(index) + '.png')
    path_label = pjoin('data', 'label', str(index) + '.csv')
    path_dom = pjoin('data', 'dom', str(index) + '.html')

    start_time = time.clock()
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(executable_path='D:\\webdriver\\chromedriver.exe', options=options)

    # fetch label format
    element_all = pd.read_csv('format.csv', index_col=0)
    # fetch url
    print("Crawling " + str(index) + ' ' + url)
    try:
        crawl(url)
    except FunctionTimedOut:
        print("*** Time out ***\n")
    print("1/4. Successfully Crawling Url")

    # get screenshots
    try:
        S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
        driver.set_window_size(S('Width'), S('Height'))  # May need manual adjustment
        driver.find_element_by_tag_name('body').screenshot(path_org)
    except:
        print("*** Saving Screenshot Failed ***\n")
    print("2/4. Successfully Saving Screenshot")

    # get elements
    try:
        element_all = fetch_element('img', element_all)
        element_all = fetch_element('button', element_all)
        element_all = fetch_element('input', element_all)
        element_all.to_csv(path_label)
        # save dom tree
        tree = driver.execute_script("return document.documentElement.outerHTML")
        open(path_dom, 'w', encoding="utf-8").write(tree)
    except:
        print("*** Catching Element Failed ***\n")
    print("3/4. Successfully Fetching Elements")

    # draw results
    pic = cv2.imread(path_org)
    # Sidong edit
    # check unmatch screenshot
    if pic.shape[0] != S('Height') or pic.shape[1] != S('Width'):
        print("*** Catching Element Failed ***\n")
        os.remove(path_label)
        os.remove(path_dom)
        os.remove(path_org)
    draw(element_all, pic)
    cv2.imwrite(path_drawn, pic)
    print("4/4. Successfully Drawn Elements")

    print("Time taken:%ds" % int(time.clock() - start_time))
    print(time.ctime() + '\n')

