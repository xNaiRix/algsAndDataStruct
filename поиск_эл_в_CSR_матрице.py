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
arr = [[3, 7, 8, 9, 15, 16], [1, 3, 2, 0, 2, 3], [0, 2, 3, 3, 6]]
print(getEl(arr, 0, 1))
for i in range(4):
    for j in range(4):
        print(getEl(arr, i, j), end = ' ')
    print()
