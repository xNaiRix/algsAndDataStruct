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
def mySort(arr):#[)
    if len(arr) == 1:
        return arr
    m = len(arr)//2
    left = mySort(arr[:m])
    right = mySort(arr[m:])
    return merge(left, right)

arr = list(map(int, input().split(',')))
print(mySort(arr))
    