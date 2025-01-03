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

def quickSort(arr, l, r):
    if (r - l) <= 0:
        return arr
    i, j  = part(arr, l, r)
    arr = quickSort(arr, l, j)
    arr = quickSort(arr, i, r)
    return arr

arr = [1, 3, 2] * 100
print(quickSort(arr, 0, len(arr) - 1))