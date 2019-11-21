import matplotlib.pyplot as plt
import numpy as np

np.random.seed(0)
sampl = [np.random.uniform(low=0.88, high=1.0, size=(50,)) for i in range(3)]

labels = ['Web', 'Rico', 'Dribbble']

bplot = plt.boxplot(sampl, patch_artist=True, labels=labels)  # 设置箱型图可填充
plt.title('Recall of UI component Detector')

colors = ['pink', 'lightblue', 'lightgreen']
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)  # 为不同的箱型图填充不同的颜色

plt.xlabel('Datasets')
plt.ylabel('Observed values')
plt.show()