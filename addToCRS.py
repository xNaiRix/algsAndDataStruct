#работает (можно ещё доработать, чтобы вправа модно было бесконечно много нулей было)
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
def add(el, i, j, arr):
    id = getId(arr, i, j)
    if id != -1:#элемент уже есть (не ноль)
        arr[0][id] = el
        return arr
    #если ноль
    id = arr[2][i]
    arr[2].pop()
    if i + 1 < len(arr[2]) and arr[2][i] == arr[2][i + 1]:
        arr[0] = arr[0][:id] + [el] + arr[0][id:]
        arr[1] = arr[1][:id] + [j] + arr[1][id:]
        for k in range(i + 1, len(arr[2])):
            arr[2][k] += 1
        arr[2].append(len(arr[0]))
        return arr
    l = len(arr[0])
    if i + 1 < len(arr[2]):
        l = min(l, arr[2][i + 1])
    for k in range(id, l):
        if arr[1][k] > j:
            arr[0] = arr[0][:k] + [el] + arr[0][k:]
            arr[1] = arr[1][:k] + [j] + arr[1][k:]
            for t in range(i + 1, len(arr[2])):
                arr[2][t] += 1
            arr[2].append(len(arr[0]))
            return arr
    arr[0] = arr[0][:l] + [el] + arr[0][l:]
    arr[1] += arr[1][:l] + [j] + arr[1][l:]
    for k in range(i + 1, len(arr[2])):
        arr[2][k] += 1
    arr[2].append(len(arr[0]))
    return arr 
arr = [[3, 7, 8, 9, 15, 16], [1, 3, 2, 0, 2, 3], [0, 2, 3, 3, 6]]
arr = add(10, 1, 1, arr)
for i in range(4):
    for j in range(4):
        print(getEl(arr,i,j), end = ' ')
    print()
