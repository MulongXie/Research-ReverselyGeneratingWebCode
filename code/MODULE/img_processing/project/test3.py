import numpy as np

class a:
    def __init__(self):
        self.p = 1
        self.q = self.p + 1

    def f(self):
        self.p = 3


a = a()

print(a.p, a.q)

a.f()

print(a.p, a.q)