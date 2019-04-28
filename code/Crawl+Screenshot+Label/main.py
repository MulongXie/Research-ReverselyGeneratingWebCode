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

# "file://D:/git_file/github/doing/Research-ReverselyGeneratingWebCode/code/selenium/page/test2.html"
initial_url = "http://yahoo.com"
link_num = 1

if is_crawl_link:
    links = crawl.crawl(initial_url, link_num, 5)
    crawl.save_links(links, 'links.csv')

if is_read_existed_links:
    csv = pd.read_csv('preset_links.csv')
    links = "http://" + csv.URL
    # links = links[2:3]
else:
    csv = pd.read_csv('links.csv')
    links = csv.link

print("*** Links Fetched ***\n")

# set the format of libel
libel_format = pd.read_csv('format.csv', index_col=0)
libel_format = libel_format.drop(libel_format.index)
for i in range(0, len(links)):
    # output path
    label = 'label/element' + str(i) + '.csv'
    img = 'screenshot/web' + str(i) + '.png'
    # catch, label and framework
    if is_catch_element:
        catch.catch(links.iloc[i], label, img, libel_format)
    if is_draw_label:
        draw.label(label, img, i)
    if is_wireframe:
        draw.wireframe(label, img, i)

if is_show_img:
    draw.show()
