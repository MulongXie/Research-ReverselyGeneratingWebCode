from selenium import webdriver
import pandas as pd


def find_element(element, df):
    div = driver.find_elements_by_xpath('//' + element)
    for d in div:
        # skim all hidden elements
        display = d.value_of_css_property('display')
        if display == 'none':
            continue
        # skim all nonsense elements
        if d.size['width'] == 0 or d.size['height'] == 0:
            continue

        dic = {}
        dic['element'] = element
        dic['p'] = 1
        dic['bx'] = d.location['x']
        dic['by'] = d.location['y']
        dic['bw'] = d.size['width']
        dic['bh'] = d.size['height']
        dic['c_' + element] = 1
        df = df.append(dic, True)
    return df


csv = pd.read_csv("test1.csv", index_col=0)
csv = csv.drop(csv.index)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get("https://services.anu.edu.au/campus-environment/safety-security")
# driver.get("file://D:/git_file/github/doing/Research-ReverselyGeneratingWebCode/code/selenium/page/test.html")

# csv = find_element('div', csv)
csv = find_element('img', csv)
csv = find_element('a', csv)
csv = find_element('h1', csv)
csv = find_element('h2', csv)
csv = find_element('button', csv)
csv = find_element('input', csv)

scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
driver.set_window_size(scroll_width, scroll_height)
driver.save_screenshot('web.png')
csv.to_csv('test2.csv')
driver.quit()