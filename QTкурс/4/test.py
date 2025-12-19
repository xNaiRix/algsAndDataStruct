from factory import *

def test_recursion():
    # 1. Данные (Имитация чтения JSON)
    fake_json = {
        "type": "group",
        "pos": [100, 100],
        "children": [
            {
                "type": "rect",
                "pos": [10, 10], # Локально в группе
                "props": {"x": 0, "y": 0, "w": 50, "h": 50, "color": "red"}
            },
            {
                "type": "group", # Вложенная группа!
                "pos": [60, 10],
                "children": [
                    {
                        "type": "line",
                        "pos": [0, 0],
                        "props": {"x1": 0, "y1": 0, "x2": 20, "y2": 20, "color": "blue"}
                    }
                ]
            }
        ]
    }

    # 2. Восстановление
    item = ShapeFactory.from_dict(fake_json)
    
    # 3. Проверка
    print(f"Created: {item}") # Должен быть Group
    print(f"Children count: {len(item.childItems())}") # Должно быть 2
    
    # Добавьте item на сцену, чтобы проверить визуально
    # scene.addItem(item)

test_recursion()#DONE