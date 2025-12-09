import copy
class TLogElement:
    def __init__(self,nextEl=None, nextIn=None):
        self.__in1 = False
        self.__in2 = False
        self._res = False
        if not hasattr(self, "calc"):
            raise NotImplementedError("Нельзя создать такой объект!")
        if nextEl and nextIn:
            self.link(nextEl, nextIn)

    def  __setIn1(self, newIn1):
        self.__in1 = newIn1
        self.calc()
        if hasattr(self,"_nextEl"):
            if self._nextIn ==1:
                self._nextEl.In1 = self._res
            elif self._nextIn == 2:
                self._nextEl.In2 = self._res
    
    def  __setIn2(self, newIn2):
        self.__in2 = newIn2
        self.calc()#посчитали Res
        if  hasattr(self,"_nextEl"):
            if self._nextIn ==1:
                self._nextEl.In1 = self._res
            elif self._nextIn == 2:
                self._nextEl.In2 = self._res
            else:
                print("Too much inputs")
    def link(self, nextEl, nextIn):
        self._nextEl = nextEl
        self._nextIn = nextIn
    In1=property(lambda x: x.__in1, __setIn1)
    In2=property(lambda x: x.__in2, __setIn2)
    Res=property(lambda x: x._res)

class TNot(TLogElement):
    def __init__(self, nextEl=None, nextIn=None):
        TLogElement.__init__(self, nextEl, nextIn)
    def calc(self):
        self._res = not self.In1
class TRepeat(TLogElement):
    def __init__(self, nextEl=None, nextIn=None):
        TLogElement.__init__(self, nextEl, nextIn)
    def calc(self):
        self._res = self.In1

class TLog2In(TLogElement):
    pass

class TAnd(TLog2In):
    def __init__(self, nextEl=None, nextIn=None):
        TLog2In.__init__(self, nextEl, nextIn)
    def calc(self):
        self._res = self.In1 and self.In2

class TOr(TLog2In):
    def __init__(self, nextEl=None, nextIn=None):
        TLog2In.__init__(self, nextEl, nextIn)
    def calc(self):
        self._res = self.In1 or self.In2

class TLogDiagram():
    def __init__(self, inputs_cnt=0):
        self.__inputs = [0] * inputs_cnt
        self.__logElements = []
        self.__startElements = []#массив вида [индекс элементы, [массив входов элемента - индексы в __inputs]], [...]
        self.__out = False
        self.__lastElement = None#индекс

    def addInp(self, newInp):
        self.__inputs.append(newInp)
    def getInpCnt(self): return len(self.inputs)
    def setInp(self, inp):
        self.__inputs=inp

    def addLogElement(self, newLogElement):
        self.__logElements.append(newLogElement)
    def addLogElements(self, newLogElements):
        self.__logElements += newLogElements
    def setLogElement(self, ind, newLogElement):
        self.__logElements[ind] = newLogElement
    def addStartElement(self, ind, inputs):
        self.__startElements.append([ind, inputs])
    
    def setLastElement(self, ind):
        self.__lastElement = ind

    def calc(self):
        for start_el, inputs in self.startElements:
            for i in range(len(inputs)):
                exec(f"self.logElements[start_el].In{i + 1}=self.inputs[{inputs[i]}]")
        self.__out = self.logElements[self.lastElement].Res

    
    def __getRes(self):
        self.calc()
        return bool(self.__out)
    
    logElements = property(lambda x: x.__logElements)
    startElements = property(lambda x: x.__startElements)
    lastElement = property(lambda x: x.__lastElement)
    inputs = property(lambda x:x.__inputs)
    out = property(__getRes)

elNot = TNot()
elAnd = TAnd(elNot, 1)
#not(a&B)
Nand = TLogDiagram(2)
Nand.addLogElements([elNot1:=TNot(),TAnd(elNot1, 1)])
Nand.addStartElement(1, [0,1])#те элементы, который подключаются к каналам ввода. Порядок важен!
Nand.setLastElement(0)

XOR = TLogDiagram(2)
#a xor b = (not(a)1 and3 b2 ) or7 (not(b)4) and6 a5
XOR.addLogElements([or7:= TOr(), and3:=TAnd(or7, 1), and6:= TAnd(or7, 2),
                             not1:= TNot(and3, 1), repeat2:=TRepeat(and3, 2),
                             not4 := TNot(and6, 1), repeat5 := TRepeat(and6, 2)])#3,4,5,6
XOR.addStartElement(3, [0])#not1
XOR.addStartElement(4, [1])#repeat2
XOR.addStartElement(5, [1])#not4
XOR.addStartElement(6, [0])#repeat5
XOR.setLastElement(0)


NOR = TLogDiagram(2)
Nand.addLogElements([elNot1:=TNot(),TOr(elNot1, 1)])
Nand.addStartElement(1, [0,1])#те элементы, который подключаются к каналам ввода. Порядок важен!
Nand.setLastElement(0)

trigger = TLogDiagram(2)
nor1 = copy.copy(NOR)#2 входа, 1 выход
nor2 = copy.copy(NOR)#2 входа, 1 выход

# 
#repeat0--- nor3 --
#   
#repeat1---nor2 --
#

trigger.addLogElements([])
print("  A | B | NAND | NAND | XOR")
for A in range(2):
    elAnd.In1 = bool(A)
    for B in range(2):
        elAnd.In2 = bool(B)
        Nand.setInp([A,B])
        XOR.setInp([A,B])
        print ( " ", A, "|", B, "| ", int(elNot.Res),"  | ", int(Nand.out),"  | ", int(XOR.out))
