from bs4 import BeautifulSoup as bs
import urllib.request as url
import pandas as pd

resp = url.urlopen('file:D:\git_file\github\doing\Research-ReverselyGeneratingWebCode\code\MODULE\webcrawler\links.html')
content = resp.read()

soup = bs(content, 'html.parser')
links = soup.find_all('a')

csv = pd.DataFrame(columns=['link'])

for i, l in enumerate(links):
    csv.loc[i] = l['href']

print(csv)
csv.to_csv('preset_links_500.csv')