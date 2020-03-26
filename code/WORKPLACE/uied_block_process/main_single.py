import ip_region_proposal as ip

resize_by_height = 800

# set input image path
# input_path_img = 'E:\\Mulong\\Datasets\\rico\\combined\\1186.jpg'
input_path_img = 'data\\input\\test.png'
output_root = 'data\\output'

ip.block_detection(input_path_img, output_root, resize_by_height=resize_by_height, show=True)

