f = open("D:\\Sirius\\Informatics\\4sem\\Ege_inf_probniky\\profimatika_11_march\\9.txt")
for i, line in enumerate(f):
    nums = [int(x) for x in line.split()]
    one = {x for x in nums if nums.count(x) == 1}
    three = {x for x in nums if nums.count(x) == 3}
    # if three and one and abs(max(nums))%10 == 0: 
    #     print("\nне пуст", nums, one, three)
    #     input()
   # print(nums, one, three)
    #input()
    if len(one) == 4 and max(nums)%10 == 0 and nums.count(max(nums)) == 3:
    #if max(nums) in three and max(nums)%10 == 0:
        print(i + 1, "строка:", line)
        break
    
#не пуст [920, 206, -428, -663, 782, 920, 920] {-663, -428, 206, 782} {920}
