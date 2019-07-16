import pandas as pd

components = pd.read_csv('output/corners.csv', index_col=0)
for i in range(len(components)):
    print(components.iloc[i]['width'])