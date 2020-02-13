import ip_region_proposal as ip
import time

resize_by_height = 800

# set input image path
PATH_IMG_INPUT = 'data\\input\\175.jpg'
PATH_OUTPUT_ROOT = 'data\\output'

start = time.clock()
ip.compo_detection(PATH_IMG_INPUT, PATH_OUTPUT_ROOT, resize_by_height)
print('Time Taken:%.3f s\n' % (time.clock() - start))
