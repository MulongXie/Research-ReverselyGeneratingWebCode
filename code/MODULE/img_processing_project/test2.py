

def f(i):
    i = 100
    return i

l = [1,2,3,4]
l[0] = f(l[0])
print(l)