import multiprocessing
import time


def func(msg):
    print(msg)
    time.sleep(1)


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=4)
    for i in range(10):
        pool.apply_async(func, ('hello', ))
    pool.close()
    pool.join()

