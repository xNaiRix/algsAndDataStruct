from math import ceil
ln = 210
cnt = 952500
memory_byte = 131 * 1024*1024
for bits_cnt in range(1, 100):
    number_bits = ln* bits_cnt
    number_bytes = ceil(number_bits/8)
    if number_bytes * cnt > memory_byte:
        print("битов на символ:",bits_cnt)
        break#6
#2^5 = 32
#32 + 1 = 33
