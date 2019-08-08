from selenium import webdriver
from func_timeout import func_set_timeout, FunctionTimedOut

@func_set_timeout(60)
def f():
    driver = webdriver.Chrome('D:/webdriver/chromedriver.exe')
    driver.set_page_load_timeout(30)

    driver.get('http://anu.edu.au ')
    print('aa')
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
    driver.save_screenshot('a.png')


f()