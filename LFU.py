class CustomDeque:
    def __init__(self, el = None, next = None, prev = None,head = None, last = None, len = 0, list = None):
        if list != None:
            self.len = list.len
            self.el = list.el
            self.next = list.next
            self.prev = list.prev
            self.head = list.head
            self.last = list.last
            return
        self.len = len#self хранит корректные хначения len, head, last
        self.el = el
        self.next = next
        self.prev = prev
        self.head = head
        self.last = last#в голове очереди всегда ахранится корректное значение последнего
    #геттеры и сетеры
    #get_front()
    def get_front(self):
        if self.len == 0:
            raise IndexError
        return self.head.el
    #change_first(): меняет и возвращает старое значение
    def change_front(self, new_el):
        if self.len == 0:
            raise IndexError
        tmp = self.head.el
        self.head.el = new_el
        return tmp
    #get_back()
    def get_back(self):
        if self.len == 0:
            raise IndexError
        return self.last.el
    #change_back()
    def change_back(self, new_el):
        if self.len == 0:
            raise IndexError
        tmp = self.last.el
        self.last.el = new_el
        return tmp
    def empty(self):
        return self.len == 0
    #добавление и удаление новых эелементов
    def push_front(self, new_el):
        if self.len == 0:
            self.len = 1
            self.head = CustomDeque(el=new_el)
            self.last = self.head
            return
        if self.len == 1:
            self.len = 2
            self.head = CustomDeque(el=new_el,next = self.last)
            self.last.prev = self.head
            return
        self.len += 1
        self.head = CustomDeque(el=new_el,next = self.head)
        self.head.next.prev = self.head
    #pop_front()
    def pop_front(self):
        if self.len == 0:
            raise IndexError
        if self.len == 1:
            tmp = self.head.el
            self.head = None
            self.len = 0
            self.last = None
            return tmp
        tmp = self.head.el
        self.head = self.head.next
        self.head.prev = None
        self.len -=1
        return tmp
    #push_back()
    def push_back(self, new_el):
        if self.len == 0:
            self.len = 1
            self.last = CustomDeque(el=new_el)
            self.head = self.last
            return
        if self.len == 1:
            self.len = 2
            self.last = CustomDeque(el=new_el, prev = self.head)
            self.head.next = self.last
            return
        self.len += 1
        self.last = CustomDeque(el=new_el, prev = self.last)
        self.last.prev.next = self.last
    #pop_back()
    def pop_back(self):
        if self.len == 0:
            raise IndexError
        if self.len == 1:
            tmp = self.head.el
            self.head = None
            self.last = None
            self.len = 0
            return tmp
        self.len -= 1
        tmp = self.last.el
        self.last = self.last.prev
        self.last.next = None
        return tmp
    def popNode(self, node):#именно нода
        if node.next == None and node.prev == None and self.head == node:
            self.head = None
            self.last = None
            self.len = 0
            return None
        if node.next == None:
            self.pop_back()
            return
        if node.prev == None:
            self.pop_front()
            return
        node.prev.next = node.next
        node.next.prev = node.prev
        self.len -= 1
    def pushNode(self, new_el):
        node = CustomDeque(el = new_el)
        if self.len == 0:
            self.head = node
            self.last = node
            self.len = 1
            return node
        self.head.prev = node
        node.next = self.head
        self.head = node
        if self.len == 1:
            self.last.prev = self.head
        self.len += 1
        return node

class LFU:
    def __init__(self, maxSize = 1, type_ = object):#элемент - это пара: data, ind in groups
        self.groups = []#дек, пред и следующая 
        self.maxSize = maxSize
        self.freq = []
        self.indexes = []#из индекса получаю ноду
        self.len = 0
        self.type = type_
    def get(self, ind):
        if ind >= self.len:
            raise IndexError
        node = self.indexes[ind]
        el = node.el
        self.groups[self.freq[ind]][0].popNode(node)
        prev = self.freq[ind]#в какой группе я был
        if len(self.groups[prev]) == 0:#если щас она пуста, то в ближайшую левую ставим новую ссылку на ближ правую
            if self.groups[prev][1] != None:
                self.groups[self.groups[prev][1]][2] = self.groups[prev][2]#
            if self.groups[prev][2] != None:
                self.groups[self.groups[prev][2]][1] = self.groups[prev][1]
        self.freq[ind] += 1
        if self.freq[ind] >= len(self.groups):
            self.groups.append([CustomDeque(), None, None])
        node = self.groups[self.freq[ind]][0].pushNode(el)
        if len(self.groups) >= 2:
                self.groups[-1][1] = self.groups[-2][2]
                if self.groups[-2][0].len != 0:
                    self.groups[-1][1] = len(self.groups) - 2
                self.groups[-2][2] = len(self.groups) - 1
        self.indexes[ind] = node
        return el[0]
    def add(self, new_el):
        if not isinstance(new_el, self.type):
            raise TypeError
        if self.len == 0:
            self.groups.append([CustomDeque(), None, None])
            node = self.groups[-1][0].pushNode([new_el, 0])
            self.indexes.append(node)
            self.freq.append(0)
            self.len += 1
            return
        if self.len == self.maxSize:
            ind = 0
            if self.groups[ind][0].len == 0:
                ind = self.groups[ind][2]
            if ind == None:
                raise IndexError
            el = self.groups[ind][0].pop_front()
            if self.groups[ind][0].len == 0:
                ind = self.groups[ind][2]
                self.groups[0][2] = ind
                if ind != None:
                    self.groups[ind][1] = 0
            self.freq[el[1]] = 0
            self.indexes[el[1]] = self.groups[0][0].pushNode([new_el, el[1]])
            return el[0]
        self.len += 1
        self.freq.append(0)
        node = self.groups[0][0].pushNode([new_el, len(self.indexes)])
        self.indexes.append(node)
        return None
'''
arr = LFU(4)
for i in range(6):
    print(i + 1, arr.add(i + 1), arr.groups[0][0].len)
print("===========")
print(arr.get(1), arr.groups[0][0].len)
print(arr.get(0), arr.groups[0][0].len)
print(arr.get(3), arr.groups[0][0].len)

print("===========")
for i in range(6,8):
    print(arr.add(i + 1))
print("==========")
for i in range(4):
    print(arr.get(i))
'''
print("true")