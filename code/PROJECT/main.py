import img_drawLabel as draw
import web_catchElementInfo as catch
import web_crawl as crawl

import pandas as pd
import cv2
import os

is_crawl_link = True
is_read_existed_links = not is_crawl_link
is_catch_element = True
is_draw_label = True
is_wireframe = True
is_show_img = False

# output path
# img_segment/img/index/segment/0..n.png
#                      /labeled/0..n.png
#                      /org.png
#            /label/index/label.csv
root = 'D:\datasets\dataset_webpage\data'
img_root = os.path.join(root, 'img_segment\img')
label_root =

initial_url = "https://www.ebay.com.au/b/Coles/bn_7114044189"
link_num = 1
start_pos = 0

if is_crawl_link:
    links = crawl.crawl(initial_url, link_num, 5)
    crawl.save_links(links, root + 'links.csv')
    csv = pd.read_csv(root + 'links.csv')
    links = csv.link

if is_read_existed_links:
    start_pos = 0
    csv = pd.read_csv(root + 'preset_links.csv')
    links = csv.link

print("*** Links Fetched ***\n")


# set the format of libel
libel_format = pd.read_csv(root + 'format.csv', index_col=0)
for i in range(start_pos, len(links)):

    label_path = root + 'label/' + str(i) + '.csv'
    img_path = root + 'screenshot/' + str(i) + '.png'
    labeled_img_path = root + 'labeled_img/' + str(i) + '.png'
    wireframe_path = root + 'labeled_wireframe/' + str(i) + '.png'

    # catch label and screenshot
    success = False
    if is_catch_element:
        success = catch.catch(links.iloc[i], label_path, img_path, libel_format)
    # read data
    label = pd.read_csv(label_path)
    img = cv2.imread(img_path)
    if is_draw_label and success:
        draw.label(label, img, labeled_img_path)
    if is_wireframe and success:
        draw.wireframe(label, img, wireframe_path)

if is_show_img:
    draw.show()
