import numpy as np


# transfer int into c dimensions one-hot array
def expand(label, c=5):
    # return y : (num_class, num_samples)
    y = np.eye(c)[label]
    y = np.squeeze(y)
    return y


l = [0,0,0,4,4,2,1]
# print(expand(l))
print(np.eye(5)[[0,1,1]])