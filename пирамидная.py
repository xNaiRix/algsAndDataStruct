def one_sort(arr, i, n):
    if 2*i + 1 < n:
        cur = i
        l = 2*i + 1
        r = 2*i + 2
        if l < n and arr[cur] > arr[l]:
            cur = l
        if r < n and arr[cur] > arr[r]:
            cur = r
        if cur != i:
            arr[i], arr[cur] = arr[cur], arr[i]
        one_sort(arr, 2*i + 1, n)
        one_sort(arr, 2*i + 2, n)
    return arr
arr = list(map(int, input().split(',')))
for i in range(len(arr), -1, -1):
    one_sort(arr, i, len(arr))
for i in range(len(arr) - 1, 0, -1):
    arr[i], arr[0] = arr[0], arr[i]
    #print(arr)
    one_sort(arr, 0, i)
    # print(arr)
    # print("-----------------------------------")
print(arr)
