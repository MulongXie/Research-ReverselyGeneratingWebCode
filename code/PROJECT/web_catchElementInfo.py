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


# take fully loaded screenshot
def take_screen(driver, output_path):
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


def find_element(element, df, driver):
    div = driver.find_elements_by_xpath('//' + element)
    for d in div:
        # skim all hidden elements
        # display = d.value_of_css_property('display')
        # if display == 'none':
        #     continue

        # skim all nonsense elements
        if d.size['width'] <= 1 or d.size['height'] <= 1 or d.location['x'] < 0 or d.location['y'] < 0:
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
def catch(url, out_label, out_img, libel_format, browser='PhantomJS'):
    try:
        print("*** catching element from %s ***" % url)
        csv = libel_format

        # initialize the webdriver to get the full screen-shot and attributes
        if browser == 'PhantomJS':
            driver = webdriver.PhantomJS()
        elif browser == 'Chrome':
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # do not show the browser every time
            driver = webdriver.Chrome(options=options)
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

        take_screen(driver, out_img)

        print("Catch Elements Successfully")
        return True
    except Exception as e:
        print(e)
        return False
