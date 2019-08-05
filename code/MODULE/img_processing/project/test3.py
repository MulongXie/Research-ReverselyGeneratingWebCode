import numpy as np

l = [(6,12), (1,2), (2,6)]
l.sort(key=lambda x: x[1] - x[0])

print(l)
