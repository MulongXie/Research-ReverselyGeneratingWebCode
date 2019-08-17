
label = open('label_colab.txt', 'r')

for l in label.readlines():
    print(l)
    l.replace('./', '')