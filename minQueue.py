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
class minQueue:
    def __init__(self):
        self.mn = CustomDeque()
        self.q = CustomDeque()
    def add(self, x):
        self.q.push_back(x)
        while not self.mn.empty():
            y = self.mn.get_back()
            if y > x:
                self.mn.pop_back()
            else:
                break
        self.mn.push_back(x)
    def size(self):
        return self.q.len
    def empty(self):
        return self.q.empty()
    def pop(self):
        if self.empty():
            raise IndexError
        x = self.q.pop_front()
        if x == self.mn.get_front:
            self.mn.pop_front()
    def getMin(self):
        return self.mn.get_front()
        