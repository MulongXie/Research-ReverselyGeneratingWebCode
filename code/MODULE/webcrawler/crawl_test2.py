import urllib.request as url
from bs4 import BeautifulSoup as bs
import time


def fetch_links(address, old):

    response = url.urlopen(address)
    content = response.read()

    soup = bs(content, 'html.parser')
    print(content)
    links = soup.find_all('a')

    link = 0
    for l in links:
        link = l['href']
        if link[:5] == 'http:':
            if link not in old:
                old.add(link)
                return link

    return link


def crawl(initial_link, iter_num):
    old_url = set()
    link = initial_link
    while iter_num > 0:
        print(link)
        link = fetch_links(link, old_url)
        old_url.add(link)
        iter_num -= 1


# bug:http://news.baidu.com/ns?cl=2&rn=20&tn=news&
crawl('http://news.baidu.com/ns?cl=2&rn=20&tn=news&', 5)

