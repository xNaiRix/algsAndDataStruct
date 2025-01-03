def getEl(arr, i, j):#arr:[el],[column],[cnt]
    a = 0
    n1 = arr[2][i]
    n2 = arr[2][i + 1]
    for k in range(n1, n2):
        if arr[1][k] == j:
            a = arr[0][k]
            break
    return a
def product(arr, b):
    n = len(b)
    m = len(arr[2]) - 1
    res =[0] * m
    if len(b) < max(arr[1]):
        raise Exception("Incorrect input")
    for i in range(m):
        for j in range(n):
            res[i] += b[j] * getEl(arr, i, j)
    return res

#arr = [[3, 7, 8, 9, 15, 16], [1, 3, 2, 0, 2, 3], [0, 2, 3, 3, 6]]
#b = [1, 2, 3, 4]
from sys import stdin
arr = list()
b = list()
for i in range(3):
    arr.append(list(map(int, input().split())))
for i in stdin:
    s = i.replace('\n', '')
    if s.isdigit():
        b.append(int(s))
ans = product(arr, b)
for i in ans:
    print(i)