import matplotlib.pyplot as plt
import numpy as np
import matplotlib


label_list = ['Button', 'Input Box', 'Image', 'Block']
num_list1 = [0.72, 0.98, 0.77, 1]
num_list2 = [0.22, 0.02, 0.08, 0]
num_list3 = [0.06, 0, 0.15, 0]
x = range(len(num_list1))
bar_width = 0.2
rects1 = plt.bar(left=x, height=num_list1, width=bar_width, color='green', label="Rectangle")
rects2 = plt.bar(left=[i + bar_width for i in x], height=num_list2, width=bar_width, color='yellow', label="Round")
rects3 = plt.bar(left=[i + bar_width*2 for i in x], height=num_list3, width=bar_width, color='red', label="Irregular")
plt.ylim(0, 1.5)
plt.ylabel("Proportion")
plt.xticks([index + 0.2 for index in x], label_list)
plt.xlabel("UI Components")
plt.title("Ratio of Shapes for UI Components")
plt.legend()
for rect in rects1:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), ha="center", va="bottom")
for rect in rects2:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), ha="center", va="bottom")
for rect in rects3:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), ha="center", va="bottom")


plt.show()