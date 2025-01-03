import math
def getMinRar(n):
    k = int(math.log2(n))
    minRar = math.ceil(n/(2**(max(0, k - 4))))
    return minRar
def merge(leftParts, rightParts):
    left = []
    right = []
    for i in leftParts:
        left+=i
    for i in rightParts:
        right+=i
    l = 0
    r = 0
    res = []
    while l < len(left) and r < len(right):
        if left[l] < right[r]:
            res.append(left[l])
            l += 1
        else:
            res.append(right[r])
            r += 1
    while l < len(left):
        res.append(left[l])
        l += 1
    while r < len(right):
        res.append(right[r])
        r += 1
    r = [res[:len(res)//2]] + [res[len(res)//2:]]
    return r
def mySort(arr):
    minRar = getMinRar(len(arr))
    parts = []
    cur_part = []
    for i in arr:
        if len(cur_part) < minRar:
            cur_part.append(i)
        elif len(cur_part) != 0:
            parts.append(sorted(cur_part))
            cur_part = []
    if len(cur_part) != 0:
        parts.append(sorted(cur_part))
    k = 1#размер блоков
    while k <= len(parts):
        cur_pos = 0
        while cur_pos + 2*k <= len(parts):
            parts = parts[:cur_pos] + merge(parts[cur_pos:cur_pos + k],parts[cur_pos + k: cur_pos+2*k]) + parts[cur_pos +2*k:]
            cur_pos += 2*k
        if cur_pos + k < len(arr):
            parts = parts[:cur_pos] + merge(parts[cur_pos:cur_pos+k], parts[cur_pos+k:])
        k*=2
    ans = []
    for i in parts:
        ans += i
    return ans
print(mySort([3, 1, 2] * 11))