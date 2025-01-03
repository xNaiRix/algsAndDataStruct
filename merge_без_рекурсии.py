def merge(left, right):
    l = 0
    r = 0
    res = []
    while l < len(left) and r < len(right):
        if left[l] > right[r]:
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
    return res
def mySort(arr):
    k = 1#размер блоков
    while k <= len(arr):
        cur_pos = 0
        while cur_pos + 2*k <= len(arr):
           arr = arr[:cur_pos] + merge(arr[cur_pos:cur_pos + k],arr[cur_pos + k: cur_pos+2*k]) + arr[cur_pos +2*k:]
           cur_pos += 2*k
        if cur_pos + k < len(arr):
            arr = arr[:cur_pos] + merge(arr[cur_pos:cur_pos+k], arr[cur_pos+k:])
        k*=2
    return arr
t = [1, 3, 2]*100
print(mySort(t))