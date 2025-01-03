def cmp(x, y):
    return x < y
class Heap:
    def __init__(self, myArr = None, compare = cmp):
        if myArr == None:
            self.arr = list()
            self.len = 0
            self.compare = compare
            return
        self.len = len(myArr)
        self.arr = myArr
        self.compare = compare
        for i in range(self.len - 1, -1, -1):
            self.down(i)
    def up(self, id = None):
        if id == None:
            id = self.len - 1
        while (id - 1)//2 >= 0 and  self.compare(self.arr[id], self.arr[(id - 1)//2]):
            self.arr[(id - 1)//2], self.arr[id] = self.arr[id], self.arr[(id - 1)//2]
            id = (id - 1)//2
    def down(self, id = None):
        if id == None:
            id = 0
        while id*2 + 1 < self.len and self.compare(self.arr[2*id + 1], self.arr[id]) or id*2 + 2 < self.len and self.compare(self.arr[2*id + 2], self.arr[id]):
            if id*2 + 2 < self.len:
                if self.compare(self.arr[2*id + 1], self.arr[2*id + 2]) and self.compare(self.arr[2* id + 1], self.arr[id]):
                    self.arr[id], self.arr[2*id + 1] = self.arr[2*id + 1], self.arr[id]
                    id = 2*id + 1
                elif self.compare(self.arr[2*id + 2], self.arr[2*id + 1]) and self.compare(self.arr[2* id + 2], self.arr[id]):
                    self.arr[id], self.arr[2*id + 2] = self.arr[2*id + 2], self.arr[id]
                    id = 2*id + 2
                continue
            if id*2 + 1 < self.len and self.compare(self.arr[2*id + 1], self.arr[id]):
                self.arr[2*id + 1], self.arr[id] = self.arr[id], self.arr[2*id + 1]
                id = 2*id + 1
    def add(self, new_el):
        self.arr.append(new_el)
        self.len += 1
        self.up()
    def get_min(self):
        if self.len == 0:
            return None
        return self.arr[0]
    def pop(self):
        if self.len == 0:
            raise IndexError
        first = self.arr[0]
        self.arr[0], self.arr[-1] = self.arr[-1], self.arr[0]
        self.arr.pop()
        self.len -=1 
        self.down()
        return first
    def getSorted(self):
        tmp = Heap(myArr = self.arr)
        ans = []
        for i in range(self.len):
            ans.append(tmp.pop())
        return ans
arr = Heap(myArr = list(map(int, input().split())))
print(' '.join([str(x) for x in arr.getSorted()]))