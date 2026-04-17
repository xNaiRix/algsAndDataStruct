def f(start, end, type):
    if start >= end: 
        return start == end
    if type == 1:
        return f(start+2, end, 2) + \
        f(start + 4, end,3) + f(start + 8, end, 4)
    if type == 2:
        return f(start+1, end,1) + \
        f(start + 4, end,3) + f(start + 8, end, 4)
    if type == 3:
        return f(start+1, end, 1) + \
        f(start + 2, end,2) + f(start + 8, end, 4)
    if type == 4:
        return f(start+1, end, 1) + \
            f(start + 2, end,2) + f(start + 4, end, 3)
    return f(start+1, end, 1) +  f (start+2, end, 2) + \
            f(start + 4, end,3) + f(start + 8, end, 4)


print(f(16,48, 0))
#14620 XX 41993 ПОФИКШЕНО