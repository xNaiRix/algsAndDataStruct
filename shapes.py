from math import pi

class Shape:
    def __init__(self):
        raise TypeError
    def __getPerimetr(self):
        raise TypeError
    def __getArea(self):
        raise TypeError
    perimetr = property(__getPerimetr)
    area = property(__getArea)
    def __str__(self):
        return f"perimetr= {self.perimetr:f} area= {self.area:f}"

class Circle(Shape):
    def __init__(self, r):
        if r <=0:
            raise ValueError("The side can't be negative")
        self.__r = r
    def __getPerimetr(self):
        return self.__r * 2 * pi
    perimetr = property(__getPerimetr)
    def __getArea(self):
        return self.__r**2 * pi
    area = property(__getArea)

    def __str__(self):
        return super().__str__()

class Rectangle(Shape):
    def __init__(self, sides):
        if len(sides) not in [2]:
            raise ValueError(f"{type(self)} must have 2 sides")
        if any(x <= 0 for x in sides):
            raise ValueError("The side can't be negative")
        self.__sides = sides

    def __getPerimetr(self):
        return sum(self.__sides) * 2
    perimetr= property(__getPerimetr)

    def __getArea(self):
        return self.__sides[0] * self.__sides[1]
    area = property(__getArea)

    def __getDiagonal(self):
        return sum(x**2 for x in self.__sides)**0.5
    diagonal = property(__getDiagonal)

    def __str__(self):
        return super().__str__()
    

class Square(Rectangle):
    def __init__(self, side):
        if side <= 0:
            raise ValueError("The side can't be negative")
        super().__init__([side, side])
        self.__side = side
    def __getInRadius(self):
        return self.__side/2
    inRadius = property(__getInRadius)


class Triangle(Shape):
    def __init__(self, sides):
        if len(sides) not in [3]:
            raise ValueError("Triangle must have 3 sides ")
        if any(x <= 0 for x in sides):
            raise ValueError("The side of triangle can't be negative")
        if any(sides[i] + sides[(i + 1)%3] <= sides[(i + 2)%3] for i in range(3)):
            raise ValueError(f"It can't be sides of {type(self)}: {sides}")
        self.__sides = sides
    
    def __getPerimetr(self):
        return sum(self.__sides)
    perimetr= property(__getPerimetr)

    def __getArea(self):
        p = self.perimetr/2
        ans = 1
        for s in self.__sides:
            ans *= (p - s)
        ans *= p
        return ans**0.5
    area = property(__getArea)
    
    def __getInRadius(self):
        return self.area/(self.perimetr/2)
    inRadius = property(__getInRadius)

    def __str__(self):
        return super().__str__()

t = Triangle([3,4,5])
s = Square(5)
r = Rectangle([4,6])
c = Circle(10)
for x in [t,s,r,c]:
    print(x)
for x in [t, s]:
    print("радиус вписанной окружности=", x.inRadius)