import urllib.request as url
from bs4 import BeautifulSoup as bs


# add link into the new_link stack
def fetch_links(address, new, old, stack_size):

    print(address)

    response = url.urlopen(address)
    if response.getcode() != 200:
        print('bad url')
        return
    content = response.read()

    soup = bs(content, 'html.parser')
    links = soup.find_all('a')

    for l in links:
        try:
            link = l['href']
            if link[:5] == 'http:':
                if link not in old:
                    new.add(link)
                    if len(new) >= stack_size:
                        return
        except:
            print("No href in a")


def crawl(initial_link, iter_num, stack_size):
    old_url = set()
    new_url = set()

    new_url.add(initial_link)
    while iter_num > 0:
        link = new_url.pop()
        old_url.add(link)
        fetch_links(link, new_url, old_url, stack_size)
        iter_num -= 1

        print('size of new stack:' + str(len(new_url)) + '   size of old stack:' + str(len(old_url)))


crawl('http://www.google.com', 10, 7)
