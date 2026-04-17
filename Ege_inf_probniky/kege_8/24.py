f = open("24.txt")
s = f.read()
print(len(s))
answer = s[101655:101655 + 14]
print(answer)#C1A9B8E59EDD98
print(len(answer))#14
print(sum(answer.count(x) for x in "89ABCDEF"))
alp = "123456789ABCDEF"
target = "89ABCDEF"
# mn = len(s)
# best_s = ""
# for l in range(len(s)):
#     for r in range(l, min(len(s) - 1, l + mn)):
#         cur = s[l:r + 1]
#         if all(x in alp for x in cur):
#             if sum(cur.count(x) for x in "89ABCDEF") >= 12:
#                 if mn >= len(cur):
#                     mn = len(cur)
#                     best_s = cur
#                     break
# print(mn)
# print(best_s)

mn = len(s)
cur_cnt = 0
l = 90000
while l < len(s):
    for cnt in range(min(mn, len(s) - l)):
        if s[l + cnt] not in alp:
            l = cnt + l
            break
        if s[l + cnt] in target:
            cur_cnt += 1
        if cur_cnt >= 12:
            mn = min(mn, cnt + 1)
            break
    # print("l:", l, "mn:", mn)
    # if l%50 == 0: input()
    l += 1
    cur_cnt = 0

#l: 101655 mn: 13
print("ANSWER:",mn)
        