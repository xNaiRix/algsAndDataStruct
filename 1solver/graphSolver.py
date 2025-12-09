import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Tuple, Callable
from abc import ABC, abstractmethod
from itertools import permutations

#события
#"askCntButtonOnCLick", {"entry": self.AskEntry.get()}
#"InputListEntry_dataChange", {"value":value}
#"InputListFrame_dataChanged", {"table": table}
#"InputTableGraph_changeCell", {
#                "table": table,
#                "vertCnt": len(table)
#            }
#"Func_changed", {"func": self.choiceVar.get()}
#"WaysTable_changeCell", {
            #     "table": table,
            #     "vertCnt": len(table)
            # })
#"solveEnded", {"answer":, "table":})
#"SolveButton_click", {})

class EventManager:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable):
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(callback)
    
    def publish(self, event_type: str, data=None):
        #print(event_type, data)
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                callback(data)

class Solver:
    def  __init__(self, events:EventManager):
        self.events = events
        self.vertCnt = 0
        self.graphMatrix = []
        self.graphList = [] 
        self.questionList = []
        self.func = "sum"
        self.events.subscribe("askCntButtonOnCLick", self._setVertCnt)
        self.events.subscribe("InputListFrame_dataChanged", self._setGraphList)
        self.events.subscribe("InputTableGraph_changeCell", self._setGraphMatrix)
        self.events.subscribe("Func_changed", self._setFunc)
        self.events.subscribe("WaysTable_changeCell", self._setQuestionList)
        self.events.subscribe("SolveButton_click", self.solve)

    def _setVertCnt(self, data):
        new_cnt = int(data.get("entry", "0"))
        if new_cnt >= 0:
            self.vertCnt = new_cnt
            #print("solver:", self.vertCnt)

    def _setGraphList(self, data):
        self.graphList = data["table"]
        #print("solver:",self.graphList)

    def _setGraphMatrix(self, data):
        self.graphMatrix = data["table"]
        #print("solver:",self.graphMatrix)

    def _setFunc(self, data):
        self.func = data["func"]
        #print("solver:",self.func)

    def _setQuestionList(self,data):
        self.questionList = data["table"]
        #print("solver:",self.questionList)


    def _getstrFromMatrix(self):
        s = ""
        for line in self.graphMatrix:
            for i in range(len(line)):
                if line[i] != "" and line[i] != "0" and line[i] != None:
                    s+= str(i + 1) + " "
            s = s.rstrip(" ")
            s += ","

        return s.rstrip(",")
    
    def _getstrFromList(self):
        s = ""
        for line in self.graphList:
            tmp = ' '.join(x for x in line if x.isalpha() or x.isdigit())
            s += tmp +","
        return s.rstrip(",")

    def _getSet(self, string):
        s = [frozenset(x.split()) for x in string.split(",")]
        return s
    
    def _getAlphabet(self, s):
        ans = set()
        for x in s:
            for y in x:
                for z in y:
                    ans.add(z)
        return list(ans)

    def _replace(self, s, letter, number):
        new_s = []
        alp = dict(zip(letter, number))
        for fr_s in s:
            new_fr_s = []
            for l in fr_s:
                new_fr_s.append(alp[l])
            new_s.append(frozenset(new_fr_s))
        return new_s

    def _calcFunc(self, table):
        nums = table.keys()
        letter = table.values()
        fromAlp = dict(zip(letter, nums))
        if self.func == "sum": f = sum
        elif self.func == "min": f = min
        else: f = max
        ans = []
        for fr, to in self.questionList:
            ans += [self.graphMatrix[int(fromAlp[fr]) - 1] [int(fromAlp[to]) - 1]]
        return str(f(int(x) for x in ans))
            
            


    def solve(self, data):
        table = {}
        s1 = self._getSet(self._getstrFromMatrix())
        s2 = self._getSet(self._getstrFromList())
        letters = self._getAlphabet(s2)
        nums = self._getAlphabet(s1)
        for p in permutations(letters):
            s = s2
            s = self._replace(s, p, nums)
            if set(s1) == set(s):
                table = {number:letter for number, letter in zip(nums, p)}

        answer = self._calcFunc(table)

        self.events.publish("solveEnded", {"answer":answer, "table":table})#кидаю тут ответ
        

class Frame(ABC):
    def __init__(self,root, events:EventManager, **kwargs):
        self.events = events
        self.frame = ttk.Frame(root, **kwargs)
        self.frame_conf = {}

    @abstractmethod
    def pack(self, **kwargs):
        pass

    def _packFrame(self, **kwargs):
        self.pack_forget()
        if kwargs:
            self.frame_conf = kwargs
        self.frame.pack(**self.frame_conf)
    
    @abstractmethod
    def bind(self, **kwargs):
        pass

    def pack_propagate(self, fl:bool|None = None):
        if fl == None: self.frame.pack_propagate()
        else: self.frame.pack_propagate(fl)

    def destroy(self):
        for name, widget in self.__dict__.items():
            #print(name)
            if isinstance(widget, ttk.Widget) or isinstance(widget, tk.Widget) or isinstance(widget, Frame):
                try:
                    widget.destroy()
                except:
                    continue
            elif isinstance(widget, list):
                for w in widget:
                    if isinstance(w, ttk.Widget) or isinstance(w, tk.Widget)or isinstance(w, Frame):
                        try:
                            w.destroy()
                        except:
                            continue
    
    def pack_forget(self):
        for name, widget in self.__dict__.items():
            #print(name)
            if name == "frame": continue
            if isinstance(widget, ttk.Widget) or isinstance(widget, tk.Widget) or isinstance(widget, Frame):
                try:
                    widget.pack_forget()
                except:
                    continue
            elif isinstance(widget, list):
                for w in widget:
                    if isinstance(w, ttk.Widget) or isinstance(w, tk.Widget)or isinstance(w, Frame):
                        try:
                            w.pack_forget()
                        except:
                            continue
    

class VertCntFrame(Frame):
    def __init__(self, root, events:EventManager, **kwargs):
        super().__init__(root, events, **kwargs)
        self.AskLabel = ttk.Label(self.frame, text = "Сколько вершин в графе?")
        self.AskEntry = ttk.Entry(self.frame, width = 5)
        self.AskButton = ttk.Button(self.frame, text = "Применить", width = 20, command = self._askCntButtonOnCLick)

    def pack(self, **kwargs):
        super()._packFrame(**kwargs)
        self.AskLabel.pack(side=tk.LEFT, padx = (0, 5))
        self.AskEntry.pack(side=tk.LEFT, padx = 5)
        self.AskButton.pack(side=tk.LEFT, padx = (5, 0))

    def bind(self):
        self.AskEntry.bind('<Return>', lambda event: self._askCntButtonOnCLick())

    def _askCntButtonOnCLick(self):
        self.events.publish("askCntButtonOnCLick", {"entry": self.AskEntry.get()})



class InputListEntryFrame(Frame):
    def __init__(self, root, events:EventManager,ind=0, **kwargs):
        super().__init__(root, events, **kwargs)
        self.nameEntry = ttk.Entry(self.frame, width = 3)
        self.dataEntry = ttk.Entry(self.frame, width = 20)
        self.ind = ind

        self.events.subscribe("ListEnrty_ChangeEntry", self._move)

    def pack(self, **kwargs):
        super()._packFrame(**kwargs)
        self.dataEntry.pack(side=tk.RIGHT)
        self.nameEntry.pack(side=tk.LEFT)

    def bind(self):
        self.dataEntry.bind("<Return>", lambda event: self._entryDataChange())
        self.nameEntry.bind("<Control-Right>", lambda event: self._focusData())
        self.dataEntry.bind("<Control-Left>", lambda event: self._focusName())
        self.nameEntry.bind("<Control-Up>", lambda event:self._Send("nameEntry", "up"))
        self.nameEntry.bind("<Control-Down>", lambda event:self._Send("nameEntry", "down"))
        self.dataEntry.bind("<Control-Up>", lambda event:self._Send("dataEntry", "up"))
        self.dataEntry.bind("<Control-Down>", lambda event:self._Send("dataEntry", "down"))

    def get(self):
        return self.dataEntry.get()

    def _entryDataChange(self):
        value = self.dataEntry.get().strip()
        self.events.publish("InputListEntry_dataChange", {"value":value})

    def _focusData(self):
        self.dataEntry.focus_set()
        self.dataEntry.select_range(0, tk.END)

    def _focusName(self):
        self.nameEntry.focus_set()
        self.nameEntry.select_range(0, tk.END)

    def _Send(self, col, way):
        new_ind = self.ind + (way == "down") * 2 - 1
        #print(col, way, self.ind, new_ind)
        self.events.publish("ListEnrty_ChangeEntry", {"col_name": col, "ind": new_ind})

    def _move(self, data):
        if data["ind"] != self.ind:
            return
        #print("hahaha", data)
        if data["col_name"] == "nameEntry":
            self.nameEntry.focus_set()
            self.nameEntry.select_range(0, tk.END)
        else:
            self.dataEntry.focus_set()
            self.dataEntry.select_range(0, tk.END)




class InputListGraphFrame(Frame):
    def __init__(self, root, events:EventManager, **kwargs):
        super().__init__(root, events, **kwargs)
        self.events.subscribe("askCntButtonOnCLick", self._vertCntUpdated)
        self.label = ttk.Label(self.frame, text="Список смежности по схеме")
        self.entries = list()#InputListEntryFrame
        self.events.subscribe("InputListEntry_dataChange", self._entryChange)

        
    def pack(self, **kwargs):
        super()._packFrame(**kwargs)
        self.label.pack(pady = (65, 5))
        for entry in self.entries:
            entry.pack()
            
    def bind(self):
        for entry in self.entries:
            entry.bind()

    def _vertCntUpdated(self, data):
        new_entry = int(data.get("entry", "0"))
        for entry in self.entries:
            entry.destroy()
        self.entries = []
        for i in range(new_entry):
            self.entries.append(InputListEntryFrame(self.frame, self.events, i))
        self.pack(**self.frame_conf)
        self.bind()

    def _entryChange(self, data):
        table = []#массив строк
        for entry in self.entries:
            table.append(entry.get().strip())
        self.events.publish("InputListFrame_dataChanged", {"table": [x.split() for x in table]})


class InputTableGraphFrame(Frame):
    def __init__(self, root, events:EventManager, **kwargs):
        super().__init__(root, events, **kwargs)
        self.events.subscribe("askCntButtonOnCLick", self._vertCntUpdated)
        self.label = ttk.Label(self.frame, text = "Матрица смежности с весами")
        self.Symmetric = tk.BooleanVar(value =True)
        self.checkBox = ttk.Checkbutton(self.frame,text="Граф неориентированный", variable=self.Symmetric)

        self.editing_entry = None
        self.editing_item = None
        self.editing_column = None
        self.size = 0

    def pack(self, **kwargs):
        super()._packFrame(**kwargs)
        self.label.pack(pady = 5)
        self.checkBox.pack(pady=5)
        if hasattr(self, "table"):
            self.table.pack(padx = 10, fill=tk.BOTH, pady=10)

    def bind(self):
        if hasattr(self, "table") and isinstance(self.table, ttk.Treeview):
            self.table.bind("<Double-1>", lambda event : self._changeCell(event))
        if hasattr(self, "entry") and  isinstance(self.entry, ttk.Entry):
            self.entry.bind('<Escape>', lambda event: self._cancelCellEditing())
            self.entry.bind("<Return>", lambda event : self._finishCellEditing())
            self.entry.bind("<FocusOut>", lambda event : self._finishCellEditing())
            for way in ["<Control-Left>", "<Control-Right>", "<Control-Up>", "<Control-Down>"]:
                #print(way)
                self.entry.bind(way, lambda event, w=way: self._goToNeighboreCell(w))
            self.entry.focus_set()
        

    def _goToNeighboreCell(self, way):
        column, item = self.editing_column, self.editing_item
        print("col, item, sz", column, item, self.size)
        column_int = int(column)
        item_int = int(str(item)[1:])
        print(way)
        if way in ["<Control-Left>", "<Control-Right>"]:
            column_int += (way == "<Control-Right>") *2 - 1
        else:
            item_int+= (way == "<Control-Down>") *2 - 1
        print("new_col, new_item", column_int, item_int)
        if column_int < 1  or column_int > self.size :
            print("not allowed")
            return "break"
        if item_int < 1 or item_int > self.size:
            print("not allowed")
            return "break"
        print("allowed")
        self._finishCellEditing()
        editing_column= "#" + str(column_int + 1)
        editing_item = f"I{item_int:0>3}"
        self._startCellEditing(editing_item, editing_column)
        

    def _vertCntUpdated(self, data):
        #print(data)
        new_entry = int(data.get("entry", "0"))
        self.size = new_entry
        print(self.size)
        columns = [str(i) for i in range(new_entry + 1)]
        if new_entry > 0:
            columns[0] = ""
        if hasattr(self, "table"):
            self.table.destroy()
        self.table = ttk.Treeview(self.frame, columns=columns, show='headings', height = min(10, new_entry))
        
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=20)

        for i in range(1, new_entry + 1):
            row_values = [str(i)] + [""] * (new_entry)
            self.table.insert("", tk.END, values=tuple(row_values))
        self.pack(**self.frame_conf)
        self.bind()

    def _changeCell(self, event):
        if self.editing_entry:
            self._finishCellEditing()
        
        region = self.table.identify_region(event.x, event.y)
        if region == "cell":
            column = self.table.identify_column(event.x)
            item = self.table.identify_row(event.y)
            if item and column != '#1':
                #print("item and col", item, column)#1-индексация (для колонок с 2, тк 0 не редачится)
                self._startCellEditing(item, column)

    def _startCellEditing(self, item, column):
        col_index = int(column[1:]) - 1
        current_value = self.table.item(item, 'values')[col_index]
        bbox = self.table.bbox(item, column)
        if not bbox:
            return
        self.entry = ttk.Entry(self.table, width=10)
        self.entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
        self.entry.insert(0, str(current_value))
        self.entry.select_range(0, tk.END)
        self.entry.focus()
        self.editing_item = item
        self.editing_column = col_index

        self.bind()

    def _finishCellEditing(self):
        if hasattr(self, "entry") and self.entry and self.editing_item is not None:
            new_value = self.entry.get()
            current_values = list(self.table.item(self.editing_item, 'values'))
            current_values[self.editing_column] = new_value
            self.table.item(self.editing_item, values=current_values)
            if self.Symmetric.get():
                col = int(str(self.editing_item)[1:])
                it = f"I{self.editing_column:0>3}"
                current_values = list(self.table.item(it, 'values'))
                current_values[col] = new_value
                self.table.item(it, values=current_values)
            table = self._getTable()
            self.events.publish("InputTableGraph_changeCell", {
                "table": table,
                "vertCnt": len(table)
            })
        
        self._cancelCellEditing()

    def _cancelCellEditing(self):
        if self.entry:
            self.entry.destroy()
            self.entry = None
        self.editing_item = None
        self.editing_column = None

    def _getTable(self):
        table = []
        if hasattr(self, "table") and isinstance(self.table, ttk.Treeview):
            items = self.table.get_children()
            for item in items:
                values = self.table.item(item, 'values')
                table.append(list(values)[1:])
        return table
    
class EdgesInputFrame(Frame):
    def __init__(self, root, events:EventManager, **kwargs):
        super().__init__(root, events, **kwargs)
        self.inputTableGraphFrame = InputTableGraphFrame(self.frame, events, width = 250, height = 250)
        self.inputListGraphFrame = InputListGraphFrame(self.frame, events,  width = 250, height = 250)

    def pack(self, **kwargs):
        super()._packFrame(**kwargs)
        self.inputTableGraphFrame.pack(side=tk.LEFT)
        self.inputTableGraphFrame.pack_propagate(False)
        self.inputListGraphFrame.pack(side=tk.LEFT)
        self.inputListGraphFrame.pack_propagate(False)

    def bind(self):
        self.inputListGraphFrame.bind()
        self.inputTableGraphFrame.bind()
    

class InputFrame(Frame):
    def __init__(self, root, events:EventManager, **kwargs):
        super().__init__(root, events, **kwargs)
        self.vertCntFrame = VertCntFrame(self.frame, events)
        self.edgesInputFrame = EdgesInputFrame(self.frame, events)

    def pack(self, **kwargs):
        super()._packFrame(**kwargs)
        self.vertCntFrame.pack(fill = tk.X, pady = 10, padx = 100)
        self.edgesInputFrame.pack(fill = tk.X)
        self.edgesInputFrame.pack()

    def bind(self):
        self.vertCntFrame.bind()
        self.edgesInputFrame.bind()



class WaysFrame(Frame):
    def __init__(self, root, events:EventManager, **kwargs):
        super().__init__(root, events, **kwargs)
        self.table = ttk.Treeview(self.frame, columns = ["from", "to"], show="headings", height = 5)
        columns = {"from": "от", "to":"до"}
        for col, text in columns.items():
            self.table.heading(col, text=text)
            self.table.column(col, width=50)
        self.editing_entry = None
        self.editing_item = None
        self.editing_column = None
        self.size = 0
        self.addRowButton = ttk.Button(self.frame, command = self._addRow, text = "Добавить")
        self.resertButton = ttk.Button(self.frame, command = self._reset, text = "Сбросить")


    def pack(self, **kwargs):
        super()._packFrame(**kwargs)
        self.table.pack(padx = 10, fill=tk.BOTH, pady=10)
        self.addRowButton.pack()
        self.resertButton.pack()

    def bind(self):
        self.frame.bind("<Control-Shift-plus>", lambda event: self._addRow())
        self.frame.focus_set()
        self.table.bind("<Double-1>", lambda event : self._changeCell(event))
        self.table.bind("<Control-Shift-plus>", lambda event: self._addRow())
        self.table.focus_set()
        if hasattr(self, "entry") and  isinstance(self.entry, ttk.Entry):
            self.entry.bind('<Escape>', lambda event: self._cancelCellEditing())
            self.entry.bind("<Return>", lambda event : self._finishCellEditing())
            self.entry.bind("<FocusOut>", lambda event : self._finishCellEditing())
            self.entry.bind("<Control-Shift-plus>",lambda event: self._addRow())
            for way in ["<Control-Left>", "<Control-Right>", "<Control-Up>", "<Control-Down>"]:
                #print(way)
                self.entry.bind(way, lambda event, w=way: self._goToNeighboreCell(w))
            self.entry.focus_set()

    def _goToNeighboreCell(self, way):
        column, item = self.editing_column, self.editing_item
        #print("col, item, sz", column, item, self.size)
        column_int = int(column)
        item_int = int(str(item)[1:])
        #print(way)
        if way in ["<Control-Left>", "<Control-Right>"]:
            column_int += (way == "<Control-Right>") *2 - 1
        else:
            item_int+= (way == "<Control-Down>") *2 - 1
        #print("new_col, new_item", column_int, item_int)
        if column_int < 0  or column_int > 1 :
            #print("not allowed")
            return "break"
        if item_int < 1 or item_int > self.size:
            #print("not allowed")
            return "break"
        #print("allowed")
        self._finishCellEditing()
        editing_column= "#" + str(column_int + 1)
        editing_item = f"I{item_int:0>3}"
        self._startCellEditing(editing_item, editing_column)

    def _addRow(self):
        self.size += 1
        self.table.insert("", "end", values=("A", "B"))
        table = self._getTable()
        self.events.publish("WaysTable_changeCell", {
                "table": table,
                "vertCnt": len(table)
            })

    def _reset(self):
        self.size = 0
        self.table.destroy()
        columns = {"from": "от", "to":"до"}
        self.table = ttk.Treeview(self.frame, columns = ["from", "to"], show="headings", height = 5)
        for col, text in columns.items():
            self.table.heading(col, text=text)
            self.table.column(col, width=50)
        self.pack(**self.frame_conf)
        self.bind()
        table = self._getTable()
        self.events.publish("WaysTable_changeCell", {
                "table": table,
                "vertCnt": len(table)
            })

    def _changeCell(self, event):
        if self.editing_entry:
            self._finishCellEditing()
        
        region = self.table.identify_region(event.x, event.y)
        if region == "cell":
            column = self.table.identify_column(event.x)
            item = self.table.identify_row(event.y)
            if item and column != '#0':
                self._startCellEditing(item, column)

    def _startCellEditing(self, item, column):
        col_index = int(column[1:]) - 1
        current_value = self.table.item(item, 'values')[col_index]
        bbox = self.table.bbox(item, column)
        if not bbox:
            return
        self.entry = ttk.Entry(self.table, width=10)
        self.entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
        self.entry.insert(0, str(current_value))
        self.entry.select_range(0, tk.END)
        self.entry.focus()
        self.editing_item = item
        self.editing_column = col_index

        self.bind()

    def _finishCellEditing(self):
        if hasattr(self, "entry") and self.entry and self.editing_item is not None:
            new_value = self.entry.get()
            current_values = list(self.table.item(self.editing_item, 'values'))
            current_values[self.editing_column] = new_value
            self.table.item(self.editing_item, values=current_values)
            
            table = self._getTable()
            self.events.publish("WaysTable_changeCell", {
                "table": table,
                "vertCnt": len(table)
            })
        
        self._cancelCellEditing()

    def _cancelCellEditing(self):
        if self.entry:
            self.entry.destroy()
            self.entry = None
        self.editing_item = None
        self.editing_column = None

    def _getTable(self):
        table = []
        if hasattr(self, "table") and isinstance(self.table, ttk.Treeview):
            items = self.table.get_children()
            for item in items:
                values = self.table.item(item, 'values')
                table.append(list(values))
        return table
            
    def delete_last_row(self):
        if hasattr(self, "table") and isinstance(self.table, ttk.Treeview):
            # Получаем все элементы
            items = self.table.get_children()
            if items:
                # Берем последний элемент
                last_item = items[-1]
                # Удаляем его
                self.table.delete(last_item)

class FuncFrame(Frame):
    def __init__(self, root, events:EventManager, **kwargs):
        super().__init__(root, events, **kwargs)
        self.minRudioButton = ttk.Radiobutton(self.frame)
        self.choiceVar = tk.StringVar(value = "sum")
        self.sumFunc = ttk.Radiobutton(self.frame, text = "Сумма путей", variable=self.choiceVar, value = "sum", command = self._changeChoice)
        self.minFunc = ttk.Radiobutton(self.frame, text = "Минимальный путь", variable=self.choiceVar, value = "min", command = self._changeChoice)
        self.maxFunc = ttk.Radiobutton(self.frame, text = "Максимальный путь", variable=self.choiceVar, value = "max", command = self._changeChoice)

    def pack(self, **kwargs):
        super()._packFrame(**kwargs)
        self.sumFunc.pack(fill = tk.X, padx = 10)
        self.minFunc.pack(fill = tk.X,padx = 10)
        self.maxFunc.pack(fill = tk.X,padx = 10)

    def bind(self):
        pass

    def _changeChoice(self):
        self.events.publish("Func_changed", {"func": self.choiceVar.get()})


class AskFrame(Frame):
    def __init__(self, root, events:EventManager, **kwargs):
        super().__init__(root, events, **kwargs)
        self.waysFrame = WaysFrame(self.frame, events)
        self.funcFrame = FuncFrame(self.frame, events)

    def pack(self, **kwargs):
        super()._packFrame(**kwargs)
        self.waysFrame.pack()
        self.funcFrame.pack()

    def bind(self):
        self.waysFrame.bind()
        self.funcFrame.bind()



class CompareFrame(Frame):
    def __init__(self, root, events:EventManager, **kwargs):
        super().__init__(root, events, **kwargs)
        self.events.subscribe("askCntButtonOnCLick", self._vertCntUpdated)
        self.events.subscribe("solveEnded", self._updateCompare)
        self.label = ttk.Label(self.frame, text = "Матрица смежности с весами")
        self.editing_entry = None
        self.editing_item = None
        self.editing_column = None

    def pack(self, **kwargs):
        super()._packFrame(**kwargs)
        if hasattr(self, "table"):
            self.table.pack(padx = 10, fill=tk.BOTH, pady=10)

    def bind(self):
        pass

    def _vertCntUpdated(self, data):
        #print(data)
        new_entry = int(data.get("entry", "0"))
        columns = [str(i) for i in range(1, new_entry + 1)]
        if hasattr(self, "table"):
            self.table.destroy()
        self.table = ttk.Treeview(self.frame, columns=columns, show='headings', height = 1)
        
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=20)

        row_values =  [""] * (new_entry)
        self.table.insert("", tk.END, values=tuple(row_values))
        self.pack(**self.frame_conf)
        self.bind()

    def _updateCompare(self, data):
        #data: table: {num:letter,...}
        if hasattr(self, "table"):
            all_items = self.table.get_children()
            for item in all_items:
                self.table.delete(item)
            columns = self.table["columns"]
            row_values = []
            for col in columns:
                row_values.append(data["table"].get(col, "None"))
            self.table.insert("", tk.END, values=tuple(row_values))
            self.pack(**self.frame_conf)


class AnswerFrame(Frame):
    def __init__(self, root, events:EventManager, **kwargs):
        super().__init__(root, events, **kwargs)
        self.compareFrame = CompareFrame(self.frame, events)
        self.numericAnswer = ttk.Entry(self.frame, state = "readonly")
        self.solveButton = ttk.Button(self.frame, text = "Решить", command = self._solveButtonOnClick)
        self.events.subscribe("solveEnded", self._updateAnswer)

    def pack(self, **kwargs):
        super()._packFrame(**kwargs)
        self.solveButton.pack()
        self.compareFrame.pack()
        self.numericAnswer.pack()

    def bind(self):
        self.compareFrame.bind()

    def _solveButtonOnClick(self):
        self.events.publish("SolveButton_click", {})

    def _updateAnswer(self, data):
        answer = data.get("answer", "None")
        self.numericAnswer.config(state="normal")
        self.numericAnswer.delete(0, tk.END)
        self.numericAnswer.insert(0, answer)
        self.numericAnswer.config(state="readonly")



class ViewManager:
    def __init__(self, events:EventManager):
        self.events = events
        self.root = tk.Tk()
        self.configMainWindow()
        self.setStyles()
        self.inputFrame = InputFrame(self.root, events)
        self.askFrame = AskFrame(self.root, events)
        self.answerFrame = AnswerFrame(self.root, events)
        self.bind()

    def configMainWindow(self):
        self.root.title("Graph solver")
        self.root.geometry("500x600")
        self.root.resizable(True, False)

    def setStyles(self):
        style = ttk.Style()
        style.configure("Custom.TFrame", background = "#d58484")
        style.configure("ActionListFrame.TFrame", background = "#DCE6FE")
        style.configure("Custom.TButton")
        style.configure("Custom.TEntry")
        style.configure("Custom.TLabel")
    
    def pack(self):
        self.inputFrame.pack(fill = tk.X)
        self.askFrame.pack(side=tk.LEFT, pady = (0, 10), padx=(50, 10))
        self.answerFrame.pack(pady = (25, 10))

    def bind(self):
        self.inputFrame.bind()
        self.askFrame.bind()
        self.answerFrame.bind()



class GraphSolverApp:
    def __init__(self):
        self.events = EventManager()
        self.view = ViewManager(self.events)
        self.solver = Solver(self.events)
    def run(self):
        self.view.pack()
        tk.mainloop()

app = GraphSolverApp()
app.run()