import os
import numpy as np

file = open('2012_train_test.txt')
out = open('train_test.txt', 'w')

c = 0
for l in file.readlines():
    i = l[:63]
    try:
        x = open(i)
        out.write(l)
    except FileNotFoundError as e:
        print(e)
        c += 1
print(c)