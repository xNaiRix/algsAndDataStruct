ln = 4403
cnt = 5845627
memory_byte = 15*1024*1024*1024#
from math import ceil
for bits in range(1, 1000):
    if ceil(bits * ln/8) * cnt >= memory_byte:
        print(bits, "alph:", 2**bits)#6, 64
        break