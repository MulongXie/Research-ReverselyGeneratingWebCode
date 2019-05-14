from selenium import webdriver
import time
def take_screenshot(browser):
    #以下代码是将浏览器页面拉到最下面。
    browser
    browser.execute_script("""
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
    time.sleep(1)

if __name__ == "__main__":
    driver = webdriver.Ie()
    driver.get('file://D:/git_file/github/doing/Research-ReverselyGeneratingWebCode/code/selenium/page/test2.html')
    take_screenshot(driver)
    driver.save_screenshot('your name'+'.png')
    driver.quit()