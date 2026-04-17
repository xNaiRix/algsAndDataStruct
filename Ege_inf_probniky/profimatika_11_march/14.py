def cnt_nulls28(n):
    cnt = 0
    if n == 0: return 1
    while n != 0:
        if n%28 == 0: cnt += 1
        n//=28
    return cnt

s = 4 * 28**10 + 3* 28**6 + 28**3
ans = []
for x in range(28001):
    s_new = s - x
    cnt = cnt_nulls28(s_new)
    ans.append([cnt, x, s_new])
print(sorted(ans, reverse=True)[:10])

print("================")
print(28**2*3, cnt_nulls28(28**2*3))

