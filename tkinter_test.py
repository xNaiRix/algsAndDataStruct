import tkinter as tk
import random
main = tk.Tk()
canvas = tk.Canvas(main, width = 500, height = 400)
canvas.pack(padx=50, pady=50)

class Point:
    def __init__(self, x,y,size,color):
        self.x = x if isinstance(x, (int, float)) else 0
        self.y = y if isinstance(y, (int, float)) else 0
        self.size = size if isinstance(size, int) else 4
        self.color = color
    def draw(self, canvas_):
        canvas_.create_oval(self.x - self.size,
                           self.y - self.size,
                           self.x + self.size,
                           self.y + self.size,
                           fill = self.color)
        

class Line:
    def __init__(self, x0, y0, x1,y1):
        self.x0 = x0 if isinstance(x0, (int, float)) else 0
        self.y0 = y0 if isinstance(y0, (int, float)) else 0
        self.x = x1 if isinstance(x1, (int, float)) else 0
        self.y = y1 if isinstance(y1, (int, float)) else 0
    def draw(self, canvas_):
        canvas_.create_line(self.x0, self.y0, self.x, self.y, fill= "orange")

p = Point(x=200, y = 40, size= 15, color = "black")
p.draw(canvas)
print(p.x, p.y, p.size)

def user_draw(canvas, object, color = "black"):
    if object is Point:
        def draw(event):
            p = object(x=event.x, y = event.y, size= 15, color = color)
            p.draw(canvas)
        return draw
    elif object is Line:
        def draw(event):
            p = object(x0=0, y0=0, x1=event.x, y1=event.y)
            p.draw(canvas)
        return draw
    else:
        return lambda event: canvas.create_text(event.x, event.y, text="Пум пум пум")
def set_color(clr, canvas):
    canvas.bind("<Button-3>", user_draw(canvas, Point, color=clr))

def create_random_polygon(canvas):
    n = random.randint(1, 10)
    colors = ["red", "green", "black", "blue", "grey", "yellow", "orange"]
    clr = random.randint(0, len(colors))
    points = []
    for i in range(n):
        x,y = random.randint(100, 400), random.randint(100, 350)
        points.append([x,y])
    canvas.create_polygon(points, fill = colors[clr], width= 3, outline= colors[(clr+1)%len(colors)])

canvas.bind("<Button-3>", user_draw(canvas, Point, color="black"))
canvas.bind("<Button-1>", user_draw(canvas, Line))

b1= tk.Button(main, text="yellow color", command = lambda: set_color("yellow", canvas), background = "yellow")
b2= tk.Button(main, text="blue color", command = lambda: set_color("blue", canvas))
b3 = tk.Button(main, text= "Polygon", command = lambda: create_random_polygon(canvas))

b1.pack(padx=0, pady=0)
b2.pack(padx=0, pady=0)
b3.pack(padx=0, pady=0)
canvas.create_polygon([[1,1], [40, 20], [50, 100]], width = 4)
main.mainloop()