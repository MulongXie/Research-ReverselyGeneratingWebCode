def tight_set(list, thresh):
    list = sorted(list)
    list_tight = [list[0]]
    anchor = 0
    for i in range(1, len(list)):
        if list[i] - list[anchor] <= thresh:
            continue
        else:
            list_tight.append(list[i])
            anchor = i
    return list_tight


l = [1,2,3,20,24, 67, 9, 14]

print(tight_set(l, 2))
