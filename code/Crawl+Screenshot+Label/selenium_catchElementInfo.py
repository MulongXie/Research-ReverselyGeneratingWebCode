from selenium import webdriver
import pandas as pd


def find_element(element, df, driver):
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


# fetch the elements information into csv
# and save the screenshot
def catch(url, out_label, out_img, libel_format):
    try:
        print("*** catch element from %s ***" % url)
        csv = libel_format

        # initialize the webdriver to get the full screen-shot and attributes
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # do not show the browser everytime
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # fetch the attributes
        # csv = find_element('div', csv, driver)
        csv = find_element('img', csv, driver)
        csv = find_element('a', csv, driver)
        csv = find_element('h1', csv, driver)
        csv = find_element('h2', csv, driver)
        csv = find_element('button', csv, driver)
        csv = find_element('input', csv, driver)
        csv.to_csv(out_label)

        # save the full-size screen shot
        scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(scroll_width, scroll_height)
        try:
            driver.find_element_by_tag_name('body').screenshot(out_img)  # avoids scrollbar
        except Exception as e:
            driver.save_screenshot(out_img)

        print("Fetch Elements Successfully")

        return True
    except Exception as e:
        print("Fail to Fetch Elements: " + e)
        return False
