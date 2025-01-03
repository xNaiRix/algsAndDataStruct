def one_sort(arr, i, n, prev_val = None):
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
        one_sort(arr, 2*i + 1, n, arr[cur])
        one_sort(arr, 2*i + 2, n, arr[cur])
    return arr
arr = list(map(int, input().split(',')))
for i in range(len(arr), -1, -1):
    one_sort(arr, i, len(arr))
print(arr)