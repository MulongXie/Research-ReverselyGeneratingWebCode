import pandas as pd

csv = pd.read_csv('preset_links.csv')
csv.link = "https://" + csv.link

csv.to_csv('preset_links.csv')