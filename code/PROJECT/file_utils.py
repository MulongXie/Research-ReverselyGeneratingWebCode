import os
import numpy as np


def make_nonexistent_dirs(dirs):
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)
