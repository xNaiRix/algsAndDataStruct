def find_primes(n):
    primes = set()
    i = 2
    while i <= n:
        cnt = 0
        while n%i == 0: 
            n//=i
            cnt += 1
        if cnt >= 1:
            primes.add(i)
        i += 1
    return list(primes)
i = 0
for n in range(6999124, 7999124):
    primes = find_primes(n)
    if len(primes) == 2 and primes[0] * primes[1] == n:
        if all("3" in str(abs(x)) for x in primes):
            print(n, max(primes))
            i += 1
    if i == 6: break
