def getId(arr, i, j):#arr:[el],[column],[cnt]
    a = -1
    if i >= len(arr[2]):
        return a
    n1 = arr[2][i]
    if i + 1 >= len(arr[2]):
        n2 = len(arr[0])
    else:
        n2 = arr[2][i + 1]
    for k in range(n1, n2):
        if arr[1][k] == j:
            a = k
            break
    return a
def getEl(arr, i, j):#arr:[el],[column],[cnt]
    a = 0
    n1 = arr[2][i]
    if i + 1 >= len(arr[2]):
        n2 = len(arr[0])
    else:
        n2 = arr[2][i + 1]
    for k in range(n1, n2):
        if arr[1][k] == j:
            a = arr[0][k]
            break
    return a
def product(a, b, n):
    res = [[],[],[]]
    cnt = 0
    for i in range(n):
        fl = False
        res[2] += [cnt]
        for j in range(n):
            cur_el = 0
            for k in range(n):
                cur_el += getEl(a, i, k) * getEl(b, k, j)
            if cur_el != 0:
                fl = True
                res[0] += [cur_el]
                res[1] += [j]
                cnt += 1
        if not fl: res[2][-1] = cnt
    res[2] += [len(res[0])]
    return res
a = [[1,3,2,8,1], [1,2,1,0,2], [0,2,3]]
b = [[3,2,3,7,3,1], [0,1,2,2,1,2], [0,3,4]]
print(product(a, b, len(a[2])))