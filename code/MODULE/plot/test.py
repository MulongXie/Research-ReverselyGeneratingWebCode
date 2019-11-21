import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
array = [[1274,7,0, 38,1],
 [5,288,0,9,0],
 [60,0,588, 70,0],
 [25,2,5, 5917, 15],
 [ 108,8,9,437, 2781]]
df_cm = pd.DataFrame(array, index = [i for i in ['button', 'input', 'icon', 'img', 'text']],
columns = [i for i in ['button', 'input', 'icon', 'img', 'text']], dtype=int)
plt.figure(figsize = (10,7))
sn.heatmap(df_cm, annot=True, cmap="YlGnBu", fmt='g')
plt.show()