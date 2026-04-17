f = open("17.txt")
nums = [int(x) for x in f]
cnt7 = len([x for x in nums if abs(x)%10 == 7])
ans = []
for i in range(len(nums) - 1):
    a,b = nums[i], nums[i+1]
    if a * b < 0 and a + b < cnt7:
        ans.append(a+b)
print(len(ans), max(ans))
