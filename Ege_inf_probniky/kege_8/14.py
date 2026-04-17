n = 13**1402 + 11**501 - 12**51 - 2323
p = 27
cnt = 0
K = 10 + (ord("K") - ord("A"))
print(K)
while n != 0:
    if n%p > 9 and n%p <= K:#было n%9 <= K
        cnt += 1
    n//=p
print(cnt)#659 --> 436