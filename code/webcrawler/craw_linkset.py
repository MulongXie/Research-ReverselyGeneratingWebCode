import urllib.request as url
from bs4 import BeautifulSoup as bs


def fetch_links(address, new, old):

    response = url.urlopen(address)
    content = response.read()

    soup = bs(content, 'html.parser')
    links = soup.find_all('a')

    for l in links:
        link = l['href']
        if link[:5] == 'http:':
            if link not in old:
                new.add(link)


def crawl(initial_link, iter_num):
    old_url = set()
    new_url = set()

    new_url.add(initial_link)
    while iter_num > 0:
        link = new_url.pop()
        old_url.add(link)
        fetch_links(link, new_url, old_url)
        iter_num -= 1

        print(link)


crawl('http://news.baidu.com/tn=news', 5)
