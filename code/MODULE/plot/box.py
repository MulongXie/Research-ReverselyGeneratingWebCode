import matplotlib.pyplot as plt
import numpy as np

np.random.seed(19680801)
all_data = [np.random.normal(0, std, size=100) for std in range(1, 4)]
labels = ['x1', 'x2', 'x3']

bplot = plt.boxplot(all_data, patch_artist=True, labels=labels)  # 设置箱型图可填充
plt.title('Rectangular box plot')

colors = ['pink', 'lightblue', 'lightgreen']
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)  # 为不同的箱型图填充不同的颜色

plt.xlabel('Three separate samples')
plt.ylabel('Observed values')
plt.show()