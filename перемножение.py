def product(arr, b):
    n = len(b)
    m = max(arr[1]) + 1
    res = [0]*m
    for i in range(len(arr[0])):
        res[arr[2][i]] += arr[0][i] * b[arr[1][i]]
    return res
from sys import stdin
arr = list()
for i in range(3):
    arr.append(list(map(int, input().split())))
#arr = [[1, 1, 2, 3], [2, 0, 1, 2], [0, 1, 1, 2]]
b = list()#b = [2, 3, 4]
for i in stdin:
    s = i.replace('\n', '')
    if s.isdigit():
        b.append(int(s))
ans = product(arr, b)
for i in ans:
    print(i)