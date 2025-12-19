from shapes import Shape
class  TestShape(Shape):
    def __init__(self):
        super().__init__()
    def type_name(self)->str: return "test"
    def to_dict(self)->dict:return {}
t = TestShape()
print(t.type_name(), t.to_dict())