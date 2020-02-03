import time


is_compo_detection = True
is_ocr_east = True
is_merge = True

input_image = 'data/input/1.jpg'
output_root = 'data/output'

start = time.clock()

if is_compo_detection:
    import ip
    ip.compo_detection(input_image, output_root)
if is_ocr_east:
    import ocr
    ocr.east(input_image, output_root)


print('### Total Time Taken %.3f s ###' % (time.clock() - start))