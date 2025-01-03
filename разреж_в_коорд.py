from sys import stdin
def sparse(arr):
    res = [[],[],[]]
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j] != 0:
                res[0].append(arr[i][j])
                res[1].append(j)
                res[2].append(i)
    return res
arr = []
for i in stdin:
    arr.append(list(map(int, i.split())))
res = sparse(arr)
print(' '.join(str(x) for x in res[0]))
print(' '.join(str(x) for x in res[1]))
print(' '.join(str(x) for x in res[2]))