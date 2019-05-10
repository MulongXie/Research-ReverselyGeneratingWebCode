import opencv_drawLabel as draw
import selenium_catchElementInfo as catch
import crawl_limitedset as crawl
import pandas as pd

is_crawl_link = True
is_read_existed_links = not is_crawl_link
is_catch_element = True
is_draw_label = True
is_wireframe = True
is_show_img = False

root = 'D:\\datasets\\dataset_webpage\\data\\test\\'
initial_url = "https://www.anu.edu.au/"
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
libel_format = pd.read_csv('format.csv', index_col=0)
for i in range(start_pos, len(links)):
    # output path
    label = root + 'label/' + str(i) + '.csv'
    img = root + 'screenshot/' + str(i) + '.png'
    labeled_img = root + 'labeled_img/' + str(i) + '.png'
    wireframe = root + 'labeled_wireframe/' + str(i) + '.png'
    # catch, label and framework
    success = False
    if is_catch_element:
        success = catch.catch(links.iloc[i], label, img, libel_format)
    if is_draw_label and success:
        draw.label(label, img, i, labeled_img)
    if is_wireframe and success:
        draw.wireframe(label, img, i, wireframe)

if is_show_img:
    draw.show()
