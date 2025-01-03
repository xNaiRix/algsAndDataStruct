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
    def get_front(self):#return ноду
        if self.len == 0:
            raise IndexError
        return self.head
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
    def push_front(self, new_el):#возвращает ноду
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
    def pop_front(self):#возвращает ноду
        if self.len == 0:
            raise IndexError
        if self.len == 1:
            tmp = self.head.el
            self.head = None
            self.len = 0
            self.last = None
            return tmp
        tmp = self.head
        self.head = self.head.next
        self.head.prev = None
        self.len -=1
        return tmp
    #push_back()
    def push_back(self, new_el):#возвращает добавленную ноду
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
        return self.last
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
class LRU:
    def __init__(self, maxLen = 1, type_ = object):
        if maxLen <= 0:
            raise RuntimeError
        self.maxLen = maxLen
        self.type = type_
        self.ord = CustomDeque()#тут [el, ind]
        self.indexes = []
        self.len = 0
    def get(self, ind):
        if ind >= self.len:
            raise IndexError
        node = self.indexes[ind]
        self.ord.popNode(node)
        self.indexes[ind] = self.ord.push_back(node.el)
        return node.el[0]
    def add(self, new_el):
        if not isinstance(new_el, self.type):
            raise TypeError
        if self.len == self.maxLen:
            node = self.ord.get_front()
            old_el = node.el
            node.el = [new_el, node.el[1]]
            return old_el[0]
        self.len += 1
        node = self.ord.pushNode([new_el, self.len - 1])
        self.indexes.append(node)
        return None
'''
arr = LRU(4)
for i in range(6):
    print(i + 1, arr.add(i + 1))
print("===========")
print(arr.get(1))
print(arr.get(0))
print(arr.get(3))
print("===========")
for i in range(6,8):
    print(arr.add(i + 1))
print("==========")
for i in range(4):
    print(arr.get(i))
'''
print("true")

