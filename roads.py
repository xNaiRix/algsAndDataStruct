class TRoad:
    def __init__(self, length_, width_):
        if length_ > 0: self.__length = length_
        else: self.__length=0

        if width_>0: self.__width = width_
        else: self.__width = 0
    
    def __getLength(self):
        return self.__length
    
    def __getWidth(self):
        return self.__width
    length = property(__getLength)
    width = property(__getWidth)

class TCar:
    def __init__(self, road, p, v):
        self.__road = road
        self.__v = v
        self.__x = 0

        if p > 0 :self.__p = p
        else: self.__p = 0
    def move(self):
        self.__x += self.__v
        if self.__x > self.__road.length:
            self.__x=0

    def __getX(self): return self.__x
    x = property(__getX)

    def __getP(self): return self.__p
    p = property(__getP)

    def __repr__(self):
        return f'x: {self.__x}, v: {self.__v}, p: {self.__p}'

road = TRoad(60, 3)
N = 4
cars = []
for i in range(N):
    print(i)
    cars.append(TCar(road=road, p= i + 1, v=(2*(i+1))))
    print(cars[-1])
for k in range(100):
    for i in range(N):
        cars[i].move()
        #print(cars[i].x, end = " ")
    #print()

print("После 100 шагов:")
for i in range(N):
    print(cars[i].x)
    