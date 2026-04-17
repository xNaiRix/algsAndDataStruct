arr = [int(x) for x in open("17.txt")]
ans = []
mx42 = max(x for x in arr if abs(x)%100 == 42)
print(mx42)
for i in range(len(arr)-2):
    n1 = arr[i]
    n2 = arr[i+1]
    n3 = arr[i + 2]
    nums = [n1,n2,n3]
    if sum(len(str(abs(x))) == 3 and abs(x)%10 == 9\
            for x in nums) == 1:
        if sum(nums) > mx42:
            ans.append(sum(nums))
print(ans)
print(len(ans))#6
print(max(ans))#189930
