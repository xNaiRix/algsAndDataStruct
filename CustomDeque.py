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
arr = CustomDeque()
for i in range(5):
    if i %2 == 0:
        arr.push_back(i)
    else:
        arr.push_front(i)
for i in range(3):
    print(arr.pop_front())

for i in range(4, 8):
    if i %2 == 0:
        arr.push_back(i)
    else:
        arr.push_front(i)
print()  
for i in range(arr.len):
    print(arr.pop_front()) 
