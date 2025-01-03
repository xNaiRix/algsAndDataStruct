def sort_part(arr, n):
    if n <= 0:
        return arr
    max_id = 0
    for i in range(0, n):
        if arr[i] > arr[max_id]:
            max_id = i
    arr[max_id], arr[n - 1] = arr[n - 1], arr[max_id]
    sort_part(arr, n - 1)
    return arr
arr = list(map(int, input().split(',')))
print(sort_part(arr, len(arr)))