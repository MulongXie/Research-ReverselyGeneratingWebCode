import time
from func_timeout import func_set_timeout

@func_set_timeout(1)
def task():
    while True:
        print('hello world')
        time.sleep(1)

task()