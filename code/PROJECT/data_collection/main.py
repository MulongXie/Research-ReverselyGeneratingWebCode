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
is_catch_element = False
is_draw_label = False
is_convert_label = True

# img_segment/img/index/segment/0..n.png
#                      /labeled/0..n.png
#                      /org.png
#            /label/index.csv
data_position = 'D:\datasets\dataset_webpage\data'
root = os.path.join(data_position, 'img_segment')
img_root = os.path.join(root, 'img')
label_root = os.path.join(root, 'label')
driver_path = 'D:\git_file\github\doing\Research-ReverselyGeneratingWebCode\code\webdriver'

if is_crawl_link:
    # set the web crawler
    initial_url = "https://world.taobao.com/"
    link_num = 1
    # start crawling
    links = crawl.crawl(initial_url, link_num, 5)
    crawl.save_links(links, os.path.join(root, 'links.csv'))
    # read links
    csv = pd.read_csv(os.path.join(root, 'links.csv'))
    links = csv.link

if is_read_existed_links:
    # read links
    csv = pd.read_csv(os.path.join(root, 'preset_links_500.csv'))
    links = csv.link

print("*** Links Fetched ***\n")

start_pos = 1000
for index in range(start_pos, len(links)):
    start_time = time.clock()
    # set path
    index_img_root = os.path.join(img_root, str(index))
    org_img_path = os.path.join(index_img_root, 'org.png')
    seg_img_path = os.path.join(index_img_root, 'segment')
    labeled_img_path = os.path.join(index_img_root, 'labeled')
    label_path = os.path.join(label_root, str(index) + '.csv')
    # make dir if not existent
    file.make_nonexistent_dirs([index_img_root, seg_img_path, labeled_img_path])

    # catch label and screenshot img and segment them into smaller size
    catch_success = False
    if is_catch_element:
        # set the format of libel
        libel_format = pd.read_csv(os.path.join(root, 'format.csv'), index_col=0)
        url = links.iloc[index]
        catch_success = catch.catch(url, label_path, org_img_path, libel_format, driver_path)
        if catch_success:
            # remove blank components
            draw.compo_scan(org_img_path, label_path)
            # segment long images into smaller sections
            seg.segment_label(label_path, 600)
            seg.segment_img(org_img_path, seg_img_path, 600, False)
        else:
            file.remove_dirs(index_img_root)
            if os.path.exists(label_path): os.remove(label_path)

    # read and draw label on segment img
    if is_draw_label and catch_success:
        seg.segment_draw(seg_img_path, labeled_img_path, label_path, False)

    end_time = time.clock()
    print("*** Time taken:%ds ***\n" % int(end_time - start_time))

if is_convert_label:
    file.label_convert(label_root, img_root, os.path.join(root, 'label.txt'))
    file.label_refine(os.path.join(root, 'label.txt'), os.path.join(root, 'label_refine.txt'))
    file.label_colab(os.path.join(root, 'label_refine.txt'), os.path.join(root, 'label_colab.txt'))

