import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from tkinter import messagebox
from itertools import product, permutations

from abc import ABC, abstractmethod
from typing import List

class Observable(ABC):
    def __init__(self, observers:List["Observable"]|None = None):
        if observers is None: self.observers = []
        else: self.observers = observers

    def update(self):
        for observer in self.observers:
            observer.on_observer_updated()

    @abstractmethod
    def on_observer_updated(self):
        pass


    def addObserver(self, observer):
        self.observers.append(observer)


class LogicalFunc(Observable):#
    def __init__(self):
        super().__init__()
        self.variables = []
        self.string_func = ""

    def __str__(self):
        return str(self.string_func)
    
    def set_func(self, func:str):

        if isinstance(func, str):
            func = func.replace("<=", " <= ").replace("==", " == ").replace('^', " and ").replace('∧', ' and ').replace('∨', ' or ').replace('→', ' <= ').replace('≡', ' == ').replace('¬', ' not ')
            self.string_func = func
            self.variables = sorted(x for x in set(func.replace("and", "").replace("or", "").replace("<=", "").replace("==", "").replace("¬", "")
                                        .replace("(", " ").replace(")", " ").replace("not", "").split()) if x not in ["", " "])
            #print("+++++++", self.variables)
        elif func == None:
            self.string_func = None
            self.variables = []
        else:
            raise ValueError("variable func must be either a string or a function")
        self.update()

    def calc(self, p)->int|None:
        if self.string_func == None:
            return None
        try:
            f = eval(f"lambda {', '.join(p.keys())}: {self.string_func}")
            #print("--------",f"lambda {', '.join(p.keys())}: {self.string_func}")
            #print("--------", p)
            return int(f(**p))
        except Exception as e:
            print(f"Error calculating function: {e}")
            return None
    def on_observer_updated(self):
        self.update()

class View(Observable):
    def __init__(self, root, data:Observable|None = None):
        super().__init__()
        self.data = data
        self.root = root

    @abstractmethod
    def set(self, *args, **kwargs):
        pass

    def show(self, func:str, *args, **kwargs):
        if hasattr(self, 'view'):
            f = eval("self.view." + func)
            f(*args, **kwargs)


class TextView(View):
    def __init__(self, data = None):
        super().__init__(data=data)
        
    def set(self, *args, **kwargs):
        if not hasattr(self, "view"):
            self.view = ttk.Label(*args, **kwargs)
        elif self.data:
            self.view.config(text=str(self.data.text))

    def on_observer_updated(self):
        self.update()


class LogicalFuncView(View):
    def __init__(self, root):
        super().__init__(root = root, data=LogicalFunc())

    def set(self, *args, **kwargs):
        if not hasattr(self, "view"):
            self.view = ttk.Entry(self.root, *args, **kwargs)
        else: 
            self.view.config(*args, **kwargs)

    def changeText(self):
        func = self.view.get()
        self.data.set_func(func=func)
        self.update()

    def on_observer_updated(self):
        self.update()


class Table(Observable):
    def __init__(self):
        super().__init__()
        self._height_cnt = 0
        self._width_cnt = 0
        self._table = []
        self._headers = []

    def getWidth(self): return self._width_cnt
    def getHeight(self): return self._height_cnt

    def __str__(self)->str:
        return str(self.table)
    
    def __getitem__(self, index):
        i,j=index
        return self._table[i][j]
    
    def __setitem__(self, index, item):
        i,j=index
        self._table[i][j]=item

    def setHeader(self, index:int, newHeader:str):
        self._headers[index] = newHeader
    
    
    def setHeaders(self, headers:List[str]):
        self._headers = headers
        self._width_cnt = len(headers)
        self._height_cnt = 2**(len(headers) - 1)
        #print("Ураа")

    def getHeader(self, index: int)->str:
        return self._headers[index]
    
    def setTable(self, table):
        self._table = table
        self._height_cnt = len(table)
        self._width_cnt =  0 if len(table) == 0 else len(table[-1])

    def getTable(self, filter = None):
        if filter is None:
            return [tuple(x) for x in self._table]
        return [tuple(x) for x in self._table if x[-1] == filter]
    
    def deleteRow(self, index):
        if len(self._table) == 0: return 
        if index == -1:
            self._table = self._table[:-1]
            self._height_cnt -= 1
            if self._height_cnt == 0: self._width_cnt = 0
            return
        if index < 0 or index > len(self._table): return
        self._table = self._table[:index] + self._table[index+1:]
        self._height_cnt -= 1

    def setHeight(self, height):
        if height < 0: return
        if height == 0:
            self._table = []
            self._height_cnt = 0
            return
        # while height != self._height_cnt:
        #     if height < self._height_cnt:
        #         self.deleteRow(-1)
        #     else:
        #         self.addRow([None]*self._width_cnt, -1)
        self._table = []
        self._height_cnt = height
        for i in range(height):
            self._table.append([None]*self._width_cnt)

    #def setWidth(self, width=0): self._width_cnt = width
            

    def deleteColumn(self, index):
        pass

    def addRow(self, row=[], index=-1):#какой строчкой она станет? 0-индексация
        if index == -1:
            self._table.append(row)
            self._height_cnt += 1

    def addColumn(self, index, column = None):
        pass

    def on_observer_updated(self):
        pass


class WholeTruthTable(Table):
    def __init__(self, func:LogicalFunc):
        self.variable_cnt = len(func.variables)
        self.func = func
        super().__init__()

    def fillTable(self):#наблюдатель?
        #print("==============",self.func.variables, "========================")
        self.setHeaders(self.func.variables + ["F"])
        self._table = []
        for p in product([0,1], repeat = self.variable_cnt):
            self.addRow(list(p) + [ self.func.calc(dict(zip(self.func.variables, p))) ])
        #уведомить наблюдателя??
            pass
        pass

    def setFunc(self, func:LogicalFunc):
        self.func = func
        self.variable_cnt = len(func.variables)
        self.fillTable()
        self.setHeaders(func.headers + ["F"])

    def on_observer_updated(self):
        self.variable_cnt = len(self.func.variables)
        self.fillTable()
        self.update()


class InputTruthTable(Table):
    def __init__(self, func:LogicalFunc):
        super().__init__()
        self.func = func
        self.answers = []
    
    def setWidth(self):
        self._width_cnt = len(self.func.variables) + 1
        for i in range(len(self._table)):
            self._table[i].append(None)

    def calc(self):
        unknown = []
        for i in range(self.getHeight()):
            for j in range(self.getWidth()):
                if self[i,j]==None:
                    unknown.append((i,j))
        answers = []
        for x in product([0,1], repeat = len(unknown)):
            table = self._table
            for ind in range(len(unknown)):
                i,j = unknown[ind]
                table[i][j]= x[i]
            values = [t[-1] for t in table]#значения функции
            table = tuple(tuple(t[:-1:]) for t in table)#тк последний столбец - столбец функции 
            if len(table) != len(set(table)):
                continue
            for p in permutations(self.func.variables):
                if [self.func.calc(dict(zip(p, line))) for line in table] == values:
                    print(p)
                    answers.append("".join(p))
                
        self.answers = list(set(answers)) if len(set(answers)) > 0 else ["None"]
        return self.answers


class TableView(View):
    def __init__(self, root, data:Table):
        super().__init__(root=root)
        self.data=data
        
        self.context_menu = None
        self.selected_item = None
        self.row_colors = {}
        self.default_bg_color = None 
        self.selection_color = "#E0E0E0"

        self.setup_custom_styles()
    
    def set(self, *args, **kwargs):
        if not hasattr(self, "view"):
            self.view = ttk.Treeview(self.root, **kwargs)
            for var in self.data.func.variables + ["F"]:
                self.view.heading(var, text=var)
        elif self.data.func: 
            self.view.config(*args, **kwargs)
            for var in self.data.func.variables + ["F"]:
                self.view.heading(var, text=var)

    def _setup_columns(self):
        if hasattr(self.data, 'func') and hasattr(self.data.func, 'variables'):
            columns = self.data.func.variables + ["F"]
            self.view["columns"] = columns
            
            for col in columns:
                self.view.heading(col, text=col)
                self.view.column(col)
            
            for col in columns:
                name = col if not isinstance(self, AutoTableView) or col == "F" else "?"
                self.view.heading(col, text=name)
                self.view.column(col, width = 30)

    def setup_custom_styles(self):
        style = ttk.Style()
        style.map("Custom.Treeview",
                 background=[('selected', self.selection_color)],
                 foreground=[('selected', 'black')])

    def on_double_click(self, event):
        item = self.view.identify_row(event.y)
        if item:
            self.selected_item = item
            self.view.selection_set(item)
            self.toggle_row_color()

    def toggle_row_color(self):
        if not self.selected_item:
            return
        current_tags = list(self.view.item(self.selected_item, "tags"))
        color_tags = [tag for tag in current_tags if tag.startswith("color_")]
        if color_tags:
            self.reset_row_color()
        else:
            saved_color = self.row_colors.get(self.selected_item, None)
            if saved_color:
                self.set_row_color(saved_color)
            else:
                self.set_quick_color("#ADD8E6")

    def show_context_menu(self, event):
        item = self.view.identify_row(event.y)
        if item:
            self.selected_item = item
            self.view.selection_set(item)
            
            self.create_context_menu(event)
            self.context_menu.post(event.x_root, event.y_root)
    
    def create_context_menu(self, event):
        self.hide_context_menu()
        
        self.context_menu = tk.Menu(self.view, tearoff=0)
        self.context_menu.add_command(
            label="Изменить цвет строки", 
            command=self.change_row_color
        )
        self.context_menu.add_command(
            label="Удалить строку", 
            command=self.delete_row
        )

        self.context_menu.add_separator()
        color_submenu = tk.Menu(self.context_menu, tearoff=0)
        color_submenu.add_command(label="Красный", command=lambda: self.set_quick_color("#FFCCCB"))
        color_submenu.add_command(label="Зеленый", command=lambda: self.set_quick_color("#90EE90"))
        color_submenu.add_command(label="Синий", command=lambda: self.set_quick_color("#ADD8E6"))
        color_submenu.add_command(label="Желтый", command=lambda: self.set_quick_color("#FFFFE0"))
        color_submenu.add_command(label="Сбросить цвет", command=self.reset_row_color)
        self.context_menu.add_cascade(label="Быстрый выбор цвета", menu=color_submenu)
        
        self.context_menu.add_separator()
        self.context_menu.add_command(
            label="Отмена", 
            command=self.hide_context_menu
        )
    
    def change_row_color(self):
        if not self.selected_item:
            return
        current_color = self.row_colors.get(self.selected_item, "#FFFFFF")
        color_code = colorchooser.askcolor(
            title="Выберите цвет строки",
            initialcolor=current_color
        )
        if color_code:
            self.set_row_color(color_code[1])
    
    def set_quick_color(self, color):
        if self.selected_item:
            self.set_row_color(color)
    
    def set_row_color(self, color):
        if not self.selected_item:
            return
        self.row_colors[self.selected_item] = color

        tag_name = f"color_{color.replace('#', '')}"
        self.view.tag_configure(tag_name, background=color)
        self.reset_row_color()
        current_tags = list(self.view.item(self.selected_item, "tags"))
        current_tags.append(tag_name)

        self.view.item(self.selected_item, tags = current_tags)
    
    def reset_row_color(self):
        if not self.selected_item:
            return
        
        if self.selected_item in self.row_colors:
            del self.row_colors[self.selected_item]
        
        current_tags = list(self.view.item(self.selected_item, "tags"))
        color_tags = [tag for tag in current_tags if tag.startswith("color_")]
        for tag in color_tags:
            current_tags.remove(tag)
        self.view.item(self.selected_item, tags=current_tags)
    
    def delete_row(self):
        if not self.selected_item:
            return
        
        confirm = messagebox.askyesno(
            "Подтверждение", 
            "Вы уверены, что хотите удалить эту строку?"
        )
        
        if confirm:
            if self.selected_item in self.row_colors:
                del self.row_colors[self.selected_item]
            
            self.data.deleteRow(self.view.index(self.selected_item))
            self.view.delete(self.selected_item)
            self.selected_item = None
    
    def hide_context_menu(self):
        if self.context_menu:
            self.context_menu.destroy()
            self.context_menu = None


class AutoTableView(TableView):
    def __init__(self, root, func:LogicalFunc):
        data = InputTruthTable(func=func)
        super().__init__(root = root, data=data)
        self.data=data
        self.setup_custom_styles()

    def create_table(self, heightEntry):
        h = heightEntry.get()
        try:
            if h == "None":
                h = None
            else:
                h = int(h)

        except Exception as e:
            print("error when creating table: ", e)
            return
        self.data.setWidth()
        self.data.setHeight(h)
        self.view.delete(*self.view.get_children())
        self._setup_columns()
        data = self.data.getTable()
        for line in data:
            if line != []:
                self.view.insert("", "end",values=line)

    def on_double_click(self, event):#изменение значений ячеек с подтягиванием изменений в самой таблице InputTruthTable через [i,j]
        item = self.view.identify_row(event.y)
        column_id = self.view.identify_column(event.x)
        
        if item and column_id != "#0":
            column_index = int(column_id[1:]) - 1
            column_name = self.view["columns"][column_index]
            values = self.view.item(item, "values")
            current_value = values[column_index] if column_index < len(values) else ""
            self.create_edit_window(item, column_index, column_name, current_value)

    def create_edit_window(self, item, column_index, column_name, current_value):
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Редактирование {column_name}")
        edit_window.geometry("300x150")
        edit_window.resizable(False, False)
        edit_window.transient(self.root)
        edit_window.grab_set()
        edit_window.transient(self.root)
        edit_window.grab_set()
        ttk.Label(
            edit_window, 
            text=f"Введите значение для {column_name}:",
            font=("Arial", 10)
        ).pack(pady=15)
        
        entry = ttk.Entry(edit_window, font=("Arial", 12), width=20)
        entry.pack(pady=10)
        entry.insert(0, str(current_value) if current_value is not None else "")
        entry.select_range(0, tk.END)
        entry.focus()
        
        btn_frame = ttk.Frame(edit_window)
        btn_frame.pack(pady=15)

        def save_value():
            new_value = entry.get().strip()
            if new_value in ["0", "1", "", "None"]:
                values = list(self.view.item(item, "values"))
                
                if new_value in ["", "None"]:
                    values[column_index] = None
                else:
                    values[column_index] = int(new_value)
                self.view.item(item, values=values)

                row_index = self.view.index(item)
                self.data[row_index, column_index] = int(new_value)

                edit_window.destroy()
            else:
                messagebox.showerror(
                    "Ошибка", 
                    "Допустимые значения: 0, 1, пустое поле (или None)",
                    parent=edit_window
                )
                entry.focus()

        ttk.Button(
            btn_frame, 
            text="Сохранить", 
            command=save_value
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Отмена", 
            command=edit_window.destroy
        ).pack(side="left", padx=5)
        
        entry.bind("<Return>", lambda e: save_value())
        entry.bind("<Escape>", lambda e: edit_window.destroy())
    
    def calc(self, answerLabel):#вычисление ответа и запись его в answerLabel
        answers = self.data.calc()
        print(answers,answers[0], type(answers[0]))
        answerLabel.config(text= '|'.join(answers))
          
    def on_observer_updated(self):
        self._setup_columns()
        self.data.setWidth()
        self.update()

    
class HandleTableView(TableView):
    def __init__(self, root, func:LogicalFunc):
        data = WholeTruthTable(func=func)
        super().__init__(root = root, data=data)
        self.data=data
    
    def calcTable(self, filter = None):
        self.view.delete(*self.view.get_children())
        self.data.fillTable()
        self._setup_columns()
        data = self.data.getTable(filter)        
        
        for line in data:
            if line != []:
                self.view.insert("", "end",values=line)

    def on_observer_updated(self):
        self.calcTable()
        self.update()

class SolverApp:
    def __init__(self):
        self.root = tk.Tk()
        self.setWindowView()
        self.setupFrames()
        self.setupFuncFrame()
        self.setupHandleSolutionFrame()
        self.setupAutoSolutionFrame()
        tk.mainloop() 

    def setWindowView(self):
        self.root.title("Second task solver")
        self.root.geometry("1000x700")
        self.root.configure(bg="#BCD6E9")

    def setupFrames(self):
        style = ttk.Style() 
        style.configure("Custom.Frames.TFrame", background="#E0EFFA")

        self.FuncFrame = ttk.Frame(self.root, height = 56, width=600, padding = (16,16,16,16), style = "Custom.Frames.TFrame")
        self.FuncFrame.pack(fill="x", padx=30, pady=10)
        self.FuncFrame.pack_propagate(False)

        self.HandleSolutionFrame = ttk.Frame(self.root, height = 352, width = 280, padding = (32,32,32,32), style = "Custom.Frames.TFrame")
        self.HandleSolutionFrame.pack(side="left", fill="both", expand=True, padx=(30, 10), pady = (10,30))
        self.HandleSolutionFrame.pack_propagate(False)

        self.AutoSolutionFrame = ttk.Frame(self.root, height = 352, width =280, padding = (32,32,32,32), style= "Custom.Frames.TFrame")
        self.AutoSolutionFrame.pack(side="right", fill="both", expand=True, padx=(10, 30), pady = (10,30))
        self.AutoSolutionFrame.pack_propagate(False)

    def setupFuncFrame(self):
        self.FuncEntry = LogicalFuncView(self.FuncFrame)
        style = ttk.Style() 
        style.configure("Custom.TEntry", background="white")
        self.FuncEntry.set(style="Custom.TEntry")
        self.FuncEntry.show("pack",side="left", fill="x", expand=True, padx=(0, 5))
    
        style = ttk.Style()
        style.configure("Custom.TButton")
        self.FuncButton = ttk.Button(self.FuncFrame, style="Custom.TButton", text="Применить")
        self.FuncButton.pack(side="right")

        self.FuncButton.bind("<Button-1>", lambda *args: self.FuncEntry.changeText())

    def setupHandleSolutionFrame(self):

        self.HandleTable= HandleTableView(self.HandleSolutionFrame, self.FuncEntry.data)

        self.FuncEntry.data.addObserver(self.HandleTable.data)
        self.FuncEntry.addObserver(self.HandleTable)
        vars = self.HandleTable.data.func.variables + ["F"]
        self.HandleTable.set(self.HandleSolutionFrame, columns = vars, show = "headings", height = 18)

        self.HandleButtonFrame = ttk.Frame(self.HandleSolutionFrame, style = "Custom.Frames.TFrame")

        self.Show0Button = ttk.Button(self.HandleButtonFrame, text="Показать только нули",
                                       command = lambda: self.HandleTable.calcTable(0))
        self.Show1Button = ttk.Button(self.HandleButtonFrame, text = "Показать только единицы",
                                      command = lambda: self.HandleTable.calcTable(1))
        self.ShowAll = ttk.Button(self.HandleButtonFrame, text = "Показать всё",
                                  command = lambda: self.HandleTable.calcTable())
        self.HandleTable.show("pack", fill="both", expand=True)

        self.HandleTable.view.bind("<Double-Button-1>", self.HandleTable.on_double_click)
        self.HandleTable.view.bind("<Button-3>", self.HandleTable.show_context_menu)

        self.HandleButtonFrame.pack(fill=tk.X, pady=(10, 5))
        self.Show0Button.pack(side=tk.LEFT, padx=(0, 5))
        self.Show1Button.pack(side = tk.LEFT, padx=10)
        self.ShowAll.pack(side=tk.RIGHT, padx=(5, 0))

        if self.HandleTable.default_bg_color is None:
            style = ttk.Style()
            self.default_bg_color = style.lookup("Treeview", "background") or "#ffffff"
            style.configure("Custom.Treeview.Heading", 
                   background="#BCEFF6", 
                   foreground="#241c4f")
        self.HandleTable.set(style="Custom.Treeview")

        self.ThinkLabel = ttk.Label(self.HandleSolutionFrame, text = "Для заметок")
        self.ThinkLabel.pack(side = tk.LEFT, padx = (10, 20))

        self.ThinkText = tk.Text(self.HandleSolutionFrame, width = 100, height = 10)
        self.ThinkText.pack(side = tk.RIGHT, pady = 10)

    def setupAutoSolutionFrame(self):
        self.AutoTable = AutoTableView(self.AutoSolutionFrame, self.FuncEntry.data)
        self.FuncEntry.data.addObserver(self.AutoTable.data)
        self.FuncEntry.addObserver(self.AutoTable)

        vars = self.AutoTable.data.func.variables + ["F"]
        self.AutoTable.set(self.AutoSolutionFrame, columns=vars, show="headings")
        self.AutoTable.show("pack", side="top", fill="both", expand=True, pady=(0, 10))
        self.AutoTable.view.bind("<Double-Button-1>", self.AutoTable.on_double_click)
        if self.AutoTable.default_bg_color is None:
            style = ttk.Style()
            self.default_bg_color = style.lookup("Treeview", "background") or "#ffffff"
        self.AutoTable.set(style="Custom.Treeview")

        self.AutoSolutionHeightEntry = ttk.Entry(self.AutoSolutionFrame, width=10)
        self.AutoSolutionHeightEntry.pack(side="left", padx=(0, 5), pady=5)
        self.AutoSolutionHeightEntry.insert(0, "4")

        self.AutoSolutionCreateButton = ttk.Button(
            self.AutoSolutionFrame, 
            text="Создать таблицу",
            command=lambda: self.AutoTable.create_table(self.AutoSolutionHeightEntry)
        )
        self.AutoSolutionCreateButton.pack(side="left", padx=(0, 10), pady=5)

        self.autoSolutionAnswerLabel = ttk.Label(self.AutoSolutionFrame)
        
        self.AutoSolutionSolveButton = ttk.Button(
            self.AutoSolutionFrame,
            text = "Посчитать",
            command = lambda: self.AutoTable.calc(self.autoSolutionAnswerLabel))

        self.AutoSolutionSolveButton.pack(side="left", padx=(0, 10), pady=5)
        self.autoSolutionAnswerLabel.pack(side="bottom", fill="x", pady=(5, 6))
        

app = SolverApp()  
