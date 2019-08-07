import img_drawLabel as draw
import img_segment as seg
import web_catchElementInfo as catch
import web_crawl as crawl
import file_utils as file

import pandas as pd
import os
import time

is_crawl_link = False
is_read_existed_links = not is_crawl_link
is_catch_element = True
is_draw_label = True

data_position = 'E:\Mulong\Datasets\dataset_webpage\page10000'
img_root = os.path.join(data_position, 'org')
label_root = os.path.join(data_position, 'label')
drawn_root = os.path.join(data_position, 'drawn')
driver_path = 'D:\webdriver'

if is_crawl_link:
    # set the web crawler
    initial_url = "https://world.taobao.com/"
    link_num = 1
    # start crawling
    links = crawl.crawl(initial_url, link_num, 5)
    crawl.save_links(links, os.path.join(data_position, 'links.csv'))
    # read links
    csv = pd.read_csv(os.path.join(data_position, 'links.csv'))
    links = csv.link

if is_read_existed_links:
    # read links
    csv = pd.read_csv(os.path.join(data_position, 'link_10000.csv'))
    links = csv.link

print("*** %d Links Fetched ***\n" % len(links))

start_pos = 75
end_pos = 1000
for index in range(start_pos, len(links)):
    start_time = time.clock()
    # set path
    org_img_path = os.path.join(img_root, str(index) + '.png')
    drawn_img_path = os.path.join(drawn_root, str(index) + '.png')
    label_path = os.path.join(label_root, str(index) + '.csv')

    # catch label and screenshot img and segment them into smaller size
    img, label = None, None
    catch_success = False
    if is_catch_element and '.com' in links.iloc[index]:
        # set the format of libel
        libel_format = pd.read_csv(os.path.join(data_position, 'format.csv'), index_col=0)
        url = 'http://' + links.iloc[index] if 'http://' not in links.iloc[index] else links.iloc[index]
        img, label = catch.catch(url, label_path, org_img_path, libel_format, driver_path)

    # read and draw label on segment img
    if is_draw_label and img is not None and label is not None:
        draw.label(label, img, drawn_img_path)

    end_time = time.clock()
    print("*** %d Time taken:%ds ***\n" % (index, int(end_time - start_time)))

    if index > end_pos:
        break

