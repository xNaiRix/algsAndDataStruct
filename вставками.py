def mySort(arr):
    n = len(arr)
    for i in range(n - 1):
        position = i + 1
        while position > 0 and arr[position - 1] > arr[position]:
            arr[position - 1], arr[position] = arr[position], arr[position - 1]
            position -= 1
    return arr
print(mySort(eval(input())))