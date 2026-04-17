f = open("9.txt")
ans = []
for i, line in enumerate(f):
    nums = list(map(int, line.split()))
    if (i + 1)%2 != 0:
        if len(set(nums)) == len(nums):
            sm = max(nums) + min(nums)
            if 3 * sm == sum(sorted(nums)[1:-1]):
                ans.append([i + 1, nums])
print(ans)
#39835