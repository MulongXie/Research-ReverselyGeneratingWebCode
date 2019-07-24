
f = open('input/1.txt')

for i, l in enumerate(f.readlines()):
    print(i)
    print(l[:-1])