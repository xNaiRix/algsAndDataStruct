def mySort(arr):
    n = len(arr)
    for i in range(n - 1):
        min_id = i
        for j in range(i, n):
            if arr[j] <= arr[min_id]:
                min_id = j
        arr[min_id], arr[i] = arr[i], arr[min_id]
    return arr
print(mySort(eval(input())))
