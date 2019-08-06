from selenium import webdriver
import pandas as pd
import time
import os
import cv2


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
    # if compo.size['height'] + compo.location['y'] > body_size['height']:
    #     return False
    # ignore too small element
    if compo.size['width'] * compo.size['height'] < 100:
        return False
    return True


# take fully loaded screenshot
def take_screen(driver, output_path):
    try:
        # scroll down to the bottom and scroll back to the top
        # ensure all element fully loaded
        driver.execute_script("""
            (function () {
                var y = 0;
                var step = 100;
                window.scroll(0, 0);
    
                function f() {
                    if (y < document.body.scrollHeight) {
                        y += step;
                        window.scroll(0, y);
                        setTimeout(f, 100);
                    } else {
                        window.scroll(0, 0);
                        document.title += "scroll-done";
                    }
                }
    
                setTimeout(f, 1000);
            })();
        """)
        for i in range(30):
            if "scroll-done" in driver.title:
                break
            time.sleep(10)
        driver.save_screenshot(output_path)
        return True

    except:
        print('Script execution filled')
        return False


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
        dic['bx'] = compo.location['x']
        dic['by'] = compo.location['y']
        dic['bw'] = compo.size['width']
        dic['bh'] = compo.size['height']
        df = df.append(dic, True)
    return df


# fetch the elements information into csv
# and save the screenshot
def catch(url, out_label, out_img, libel_format, driver_path, browser='PhantomJS'):
    try:
        print("*** catching element from %s ***" % url)
        label = libel_format

        # initialize the webdriver to get the full screen-shot and attributes
        if browser == 'PhantomJS':
            driver = webdriver.PhantomJS(executable_path=os.path.join(driver_path, 'phantomjs.exe'))
        elif browser == 'Chrome':
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # do not show the browser every time
            driver = webdriver.Chrome(executable_path=os.path.join(driver_path, 'chromedriver.exe'), options=options)
        driver.maximize_window()
        driver.get(url)

        # fetch the attributes
        # label = find_element('div', label, driver)
        # label = find_element('img', label, driver)
        # label = find_element('a', label, driver)
        # label = find_element('h1', label, driver)
        # label = find_element('h2', label, driver)
        label = find_element('button', label, driver)
        label = find_element('input', label, driver)

        if take_screen(driver, out_img):
            img = cv2.imread(out_img)
            if img is None:
                print("Screenshot is None")
                return None, None

            label.to_csv(out_label)
            print("Catch Elements Successfully")
            return img, label
        else:
            print("Screenshot Failed")
            return None, None

    except Exception as e:
        print(e)
        return None, None


def screenshot(output_path, url, driver_path):
    driver = webdriver.PhantomJS(executable_path=os.path.join(driver_path, 'phantomjs.exe'))
    driver.get(url)
    driver.save_screenshot(output_path)