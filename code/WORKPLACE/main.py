import pandas as pd
from selenium import webdriver
import cv2
from os.path import join as pjoin


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


csv = pd.read_csv('link.csv')
links = csv.link

options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(executable_path='D:\\webdriver\\chromedriver.exe', options=options)


start_pos = 15000
end_pos = 20000
for index in range(start_pos, end_pos):
    # set output
    path_org = pjoin('data', 'org', str(index) + '.png')
    path_drawn = pjoin('data', 'drawn', str(index) + '.png')
    path_label = pjoin('data', 'label', str(index) + '.csv')

    # store label
    element_all = pd.read_csv('format.csv', index_col=0)
    # fetch url
    url = 'http://' + links.iloc[index]
    driver.get(url)
    print("*** Fetch " + url + " ***")

    # get screenshots
    body = driver.find_elements_by_tag_name('body')
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
    driver.set_window_size(S('Width'), S('Height'))  # May need manual adjustment
    driver.find_element_by_tag_name('body').screenshot(path_org)
    print("*** Save Screenshot ***")
    # get elements
    element_all = fetch_element('img', element_all)
    element_all = fetch_element('button', element_all)
    element_all = fetch_element('input', element_all)
    element_all.to_csv(path_label)
    print("*** Get Elements ***\n")

    # draw results
    pic = cv2.imread(path_org)
    draw(element_all, pic)
    cv2.imwrite(path_drawn, pic)

    break
