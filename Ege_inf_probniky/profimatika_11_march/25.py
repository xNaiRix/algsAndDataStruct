def find_divs(n):
    prime_divs = []
    n_copy = n
    i = 2
    while i <= n:
        while n%i == 0:
            n//=i
            prime_divs.append(i)
            if len(prime_divs) >= 3: break
        if len(prime_divs) >= 3: break    
        i += 1
    return prime_divs

cnt = 0
for i in range(1326234, 10000000):
    if cnt == 10: break
    divs = find_divs(i)
    if len(divs) != 2: continue
    if str(divs[0]).count("7") == 1:
        if str(divs[1]).count("7") == 1:
            print(i, divs)
            cnt += 1
# 1326269 [7, 189467]
# 1326311 [7, 189473]
# 1326353 [7, 189479]
# 1326401 [197, 6733]
# 1326527 [17, 78031]

# 1326539 [709, 1871]
# 1326569 [179, 7411]
# 1326619 [7, 189517]
# 1326697 [17, 78041]
# 1326737 [173, 7669]
    

