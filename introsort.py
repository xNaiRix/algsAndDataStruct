import math
def part(arr, l, r):
    p = arr[(l+r)//2]
    i = l
    j = r# [l;r]
    while i <= j:
        while i <= r and arr[i] < p:
            i+=1
        while j >= l and arr[j] > p:
            j-=1
        if i <= j and i <= r and j >= l:
            arr[i],arr[j] = arr[j], arr[i]
            i+=1
            j-=1
    return i, j
arr = [3, 1, 2]*100
maxDepth = math.log2(len(arr))
def quickSort(arr, l, r, depth):
    if (r - l) <= 0:
        return arr
    if depth > maxDepth:
        arr = arr[:l] + pyramid_sort(arr[l:r]) + arr[r:]
        return arr
    i, j  = part(arr, l, r)
    arr = quickSort(arr, l, j, depth + 1)
    arr = quickSort(arr, i, r, depth + 1)
    return arr
def one_sort(arr, i, n):
    if 2*i + 1 < n:
        cur = i
        l = 2*i + 1
        r = 2*i + 2
        if l < n and arr[cur] < arr[l]:
            cur = l
        if r < n and arr[cur] < arr[r]:
            cur = r
        if cur != i:
            arr[i], arr[cur] = arr[cur], arr[i]
        one_sort(arr, 2*i + 1, n)
        one_sort(arr, 2*i + 2, n)
    return arr
def pyramid_sort(arr):
    for i in range(len(arr), -1, -1):
        one_sort(arr, i, len(arr))
    for i in range(len(arr) - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        one_sort(arr, 0, i)
    return arr
print(quickSort(arr, 0, len(arr) - 1, 0))