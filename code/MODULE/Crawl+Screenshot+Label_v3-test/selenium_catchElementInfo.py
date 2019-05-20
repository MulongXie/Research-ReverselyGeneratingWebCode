from selenium import webdriver
import pandas as pd
import time


# refine the data
def compo_filter(compo, body_size):
    # ignore all hidden elements
    display = compo.value_of_css_property('display')
    if display == 'none':
        return False
    # ignore all nonsense elements
    if compo.size['width'] == 0 or compo.size['height'] == 0 or compo.location['x'] < 0 or compo.location['y'] < 0:
        return False
    # ignore too large element
    if compo.size['width'] + compo.location['x'] > body_size['width']:
        return False
    if compo.size['height'] + compo.location['y'] > body_size['height']:
        return False
    # ignore too small element
    if compo.size['width'] * compo.size['height'] < 100:
        return False
    return True


def find_element(element, df, driver):
    # get body size for compo filter
    body = driver.find_elements_by_tag_name('body')
    body_size = [b.size for b in body]
    # get all components
    compos = driver.find_elements_by_xpath('//' + element)
    for compo in compos:
        if not compo_filter(compo, body_size[0]):
            continue
        dic = {}
        dic['element'] = element
        dic['p'] = 1
        dic['bx'] = compo.location['x']
        dic['by'] = compo.location['y']
        dic['bw'] = compo.size['width']
        dic['bh'] = compo.size['height']
        dic['c_' + element] = 1
        df = df.append(dic, True)
    return df


# fetch the elements information into csv
# and save the screenshot
def catch(url, out_label, out_img, libel_format, bro_driver):
    try:
        print("*** catch element from %s ***" % url)
        csv = libel_format

        # initialize the webdriver to get the full screen-shot and attributes
        if bro_driver == 0:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # do not show the browser every time
            driver = webdriver.Chrome(options=options)
            driver.maximize_window()
        else:
            driver = webdriver.PhantomJS()
            driver.maximize_window()
        driver.get(url)

        # fetch the attributes
        # csv = find_element('div', csv, driver)
        csv = find_element('img', csv, driver)
        # csv = find_element('a', csv, driver)
        # csv = find_element('h1', csv, driver)
        # csv = find_element('h2', csv, driver)
        # csv = find_element('button', csv, driver)
        # csv = find_element('input', csv, driver)
        csv.to_csv(out_label)

        if bro_driver == 0:
            scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
            scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
            width = driver.get_window_size()['width'] if driver.get_window_size()['width'] > scroll_width else scroll_width
            height = driver.get_window_size()['height'] if driver.get_window_size()['width'] > scroll_height else scroll_height
            driver.set_window_position(0, 0)
            driver.set_window_size(driver.get_window_size()['width'], scroll_height)

        print(driver.get_window_size())
        driver.save_screenshot(out_img)

        print("Fetch Elements Successfully")
        return True
    except Exception as e:
        print(e)
        return False
