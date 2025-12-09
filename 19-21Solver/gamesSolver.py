import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

#Задачи для демонстрации функционала
#задача для 2 куч: № 22066 (любой ход Пети), № 20907 (неудачный ход Пети)
#задача для 1 кучи:	№ 22437 (любой ход Пети), № 8163 (неудачный ход Пети)
class Solver:
    def __init__(self):
        self._actions = []#строки вида "s1 + 2, s2", "s1, s2 + 2", "s1*2, s2"
        self._twoHeaps = False
        self._winCnt = 0
        self._startCnt = 0
        self._endCnt = 0
        self._otherHeapCnt = 0 
        self._forAnyPetya = False
    
    def addAction(self, action_str):
        self._actions.append("[s[0] " + action_str + (", s[1]]" if self._twoHeaps else "]"))
        if self._twoHeaps:
            self._actions.append("[s[0], s[1] " + action_str + "]")
        #print(self._actions)

    def clearActions(self):
        self._actions = []

    def changeHeapsCnt(self, cnt):
        if cnt == 1:
            self._twoHeaps = False
        else:
            self._twoHeaps = True
        new_actions = []
        if not self._twoHeaps:
            for action in self._actions:
                tmp = action[:action.find(",")].replace(" ", "") + "]"
                if tmp != "[s[0]]":
                    new_actions.append(tmp)
        else:
            for action in self._actions:
                new_actions.append(action[:-1] + ", " + "s[1]]")
                new_actions.append("[s[0], " + action.replace("[0]", "[1]", 1)[1:])
        self._actions = new_actions
        #print(self._actions)
    

    def changePetyaFlag(self):
        self._forAnyPetya = not self._forAnyPetya

    def setWinCnt(self, win_cnt):
        self._winCnt = win_cnt
    
    def setInterval(self, start, end):
        self._startCnt=start
        self._endCnt = end

    def setOherHeapCnt(self, otherHeapCnt):
        self._otherHeapCnt = otherHeapCnt

    def solve(self):
        def _solve(s, m, flag= True):#s - массив из 1 или 2 элементов
            #print(s)
            if sum(s) >= self._winCnt:
                return m%2 == 0
            if m == 0: return False

            h = []
            #print(self._actions)
            for action in self._actions:
                new_s = eval(action)
                h.append(_solve(new_s, m - 1, flag))
            return any(h) if m%2 == 1 or not flag else all(h)
        
        s = []
        if self._twoHeaps:
            s.append(self._otherHeapCnt)
        task19 = [s2 for s2 in range(self._startCnt, self._endCnt + 1) if not _solve(s+ [s2], 1, self._forAnyPetya) and _solve(s+ [s2], 2, self._forAnyPetya)]
        task20 = [s2 for s2 in range(self._startCnt, self._endCnt + 1) if not _solve(s + [s2], 1) and _solve(s+ [s2], 3)]
        task21 = [s2 for s2 in range(self._startCnt, self._endCnt + 1) if not _solve(s + [s2], 2) and _solve(s+ [s2], 4)]
        return task19, task20, task21

class Frame(ABC):
    frame:ttk.Frame
    solver: Solver

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def bind(self):
        pass

    def forget(self):
        for name, var in self.__dict__.items():
            try:
                if name != "frame":
                    var.pack_forget()
            except:
                continue

class ActionsFrame(Frame):
    def __init__(self, root, solver:Solver):
        self.solver = solver

        self.frame = ttk.Frame(root, height = 350, width = 250)
        self.possibleActionsLabel = ttk.Label(self.frame, text = "Возможные действия")
        
        self.inputFrame = ttk.Frame(self.frame)
        self.possibleActionsEntry = ttk.Entry(self.inputFrame, width = 40)
        self.possibleActionsButton = ttk.Button(self.inputFrame, text = "добавить", width = 12)
        self.possibleActionsList = list()
        self.anyPetyaCheckBox = ttk.Checkbutton(self.frame, text="При любом ходе Пети")

        self.actionsListFrame = ttk.Frame(self.frame)#style = "ActionListFrame.TFrame"
        self.startInd = 0
        self.clearActionsButton = ttk.Button(self.frame, text = "Сбросить")
        

    def show(self):
        self.forget()
        self.frame.pack(side = tk.LEFT, expand=True)
        self.frame.pack_propagate(False)

        self.possibleActionsLabel.pack(pady=(10, 5), padx = (0, 80))
        self.inputFrame.pack(fill = tk.X, pady=(0,10))
        self.possibleActionsButton.pack(padx = (5, 25),side = tk.RIGHT)#side = tk.RIGHT, fill = "x", padx = (5, 50)
        self.possibleActionsEntry.pack(padx = (25, 0),side = tk.LEFT)#side = tk.LEFT, fill = "x", padx = (50, 5)
        
        if len(self.possibleActionsList) != 0:
            self.actionsListFrame.pack(padx=(5,0))
        
        for action in self.possibleActionsList:
            action.pack_forget()

        for action in self.possibleActionsList[self.startInd:min(len(self.possibleActionsList), self.startInd+8)]:
            action.pack(padx = (0, 92))
        self.clearActionsButton.pack(padx=(0,123), pady = (10,0))
        self.anyPetyaCheckBox.pack(padx=(0,53), pady = (10,0))

    
    def bind(self):
        self.possibleActionsButton.config(command = lambda: self._possibleActionButtonClick(self.solver))
        self.possibleActionsEntry.bind('<Return>', lambda event: self._possibleActionButtonClick(self.solver))
        self.anyPetyaCheckBox.config(command = lambda: self._anyPetyaCheckBoxClick(self.solver))
        self.clearActionsButton.config(command = lambda: self._clearActionsButtonClick(self.solver))
        self.actionsListFrame.bind("<MouseWheel>", self._actionsListFrameOnMousewheel)

    def _actionsListFrameOnMousewheel(self,event):
        delta = event.delta
        #print(self.startInd)
        sz = len(self.possibleActionsList)
        if delta > 0:
            self.startInd = max(0, min(max(sz - 8,0), self.startInd - 1))
        else:
            self.startInd = max(0, min(max(sz - 8,0), self.startInd + 1))
        #print(delta//120, self.startInd)
        self.show()

    
    def _possibleActionButtonClick(self, solver:Solver):
        text = self.possibleActionsEntry.get()
        solver.addAction(text)
        self.possibleActionsList.insert(0,ttk.Entry(self.actionsListFrame, width = 18))
        self.possibleActionsList[0].insert(0, text)
        self.possibleActionsList[0].config(state = "readonly")
        self.possibleActionsEntry.delete(0, tk.END)
        self.show()
        
    def _anyPetyaCheckBoxClick(self, solver:Solver):
        solver.changePetyaFlag()
   
    def _clearActionsButtonClick(self, solver:Solver):
        solver.clearActions()
        for action in self.possibleActionsList:
            action.destroy()
        self.possibleActionsList = []
        self.possibleActionsEntry.delete(0, tk.END)
        self.show()


class HeapsFrame(Frame):
    def __init__(self, root, solver:Solver):
        self.solver = solver

        self.frame = ttk.Frame(root, height = 350, width = 250)

        self.heapsCntFrame = ttk.Frame(self.frame)
        self.heapsCntLabel = ttk.Label(self.heapsCntFrame, text = "Количество куч")
        self.heapsCntVar = tk.StringVar(value = "1")
        self.heapsCntComboBox = ttk.Combobox(self.heapsCntFrame, values=["1", "2"], state="readonly",width=3)

        self.otherHeapCntFrame = ttk.Frame(self.frame)
        self.otherHeapCntLabel = ttk.Label(self.otherHeapCntFrame, text = "Камней в одной куче")
        self.otherHeapCntEntry = ttk.Entry(self.otherHeapCntFrame, width=5)

        self.heapCntDistributionLabel = ttk.Label(self.frame, text = "Диапазон камней в куче")
        self.heapCntDistributionFrame = ttk.Frame(self.frame)
        self.heapCntDistributionStartLabel = ttk.Label(self.heapCntDistributionFrame, text = "от")
        self.heapCntDistributionStartEntry = ttk.Entry(self.heapCntDistributionFrame, width = 5)
        self.heapCntDistributionEndLabel = ttk.Label(self.heapCntDistributionFrame, text = "до")
        self.heapCntDistributionEndEntry = ttk.Entry(self.heapCntDistributionFrame,width = 5)

        self.heapCntWinFrame = ttk.Frame(self.frame)
        self.heapCntWinLabel = ttk.Label(self.heapCntWinFrame, text = "Камней для победы")
        self.heapCntWinEntry = ttk.Entry(self.heapCntWinFrame, width = 5)
        

    def show(self):
        self.forget()
        self.frame.pack(side = tk.RIGHT, padx = 30, expand=True)
        self.frame.pack_propagate(False)

        self.heapsCntFrame.pack(pady = (10, 5), fill = "x")
        self.heapsCntComboBox.pack(side=tk.RIGHT, padx=(15, 25))
        self.heapsCntLabel.pack(side=tk.LEFT)

        self.heapCntWinFrame.pack(fill = "x")
        self.heapCntWinEntry.pack(side = tk.RIGHT, padx = (5,25))
        self.heapCntWinLabel.pack(side = tk.LEFT, padx=(0,10))

        if self.solver._twoHeaps:
            self.otherHeapCntFrame.pack(pady=10,fill = "x")
            self.otherHeapCntEntry.pack(side=tk.RIGHT, padx = (0, 25))
            self.otherHeapCntLabel.pack(side=tk.LEFT)
        else:
            # self.otherHeapCntEntry.pack_forget()
            # self.otherHeapCntLabel.pack_forget()
            self.otherHeapCntFrame.pack_forget()

        self.heapCntDistributionLabel.pack(fill = "x")
        self.heapCntDistributionFrame.pack(fill = "x", pady = 10)
        self.heapCntDistributionStartLabel.pack(side=tk.LEFT, padx = (0, 3))
        self.heapCntDistributionStartEntry.pack(side=tk.LEFT, padx = (3, 5))
        self.heapCntDistributionEndLabel.pack(side=tk.LEFT, padx = (45, 3))
        self.heapCntDistributionEndEntry.pack(side=tk.LEFT, padx = (2,10))

    def bind(self):
        self.heapsCntComboBox.bind("<<ComboboxSelected>>", lambda event: self._heapsCntOptionMenuSelect(self.solver))

    def _heapsCntOptionMenuSelect(self, solver:Solver):
        cnt = int(self.heapsCntComboBox.get())
        solver.changeHeapsCnt(cnt)
        self.show()
        #print(solver._twoHeaps)


class AnswerFrame(Frame):
    def __init__(self, root, solver:Solver):
        self.solver = solver
        self.frame = ttk.Frame(root, height = 160)
        self.solveButton = ttk.Button(self.frame, text="Решить")

        self.task19Entry = ttk.Entry(self.frame)
        self.task19Entry.insert(0, "Задача 19 | ")
        self.task19Entry.config(state="readonly")

        self.task20Entry = ttk.Entry(self.frame)
        self.task20Entry.insert(0, "Задача 20 | ")
        self.task20Entry.config(state="readonly")

        self.task21Entry = ttk.Entry(self.frame)
        self.task21Entry.insert(0, "Задача 21 | ")
        self.task21Entry.config(state="readonly")

    def show(self):
        self.forget()
        self.frame.pack(expand=True, fill = tk.BOTH, pady=(0,0))
        self.frame.pack_propagate(False)
        self.solveButton.pack(padx= (0, 370), pady = 10)
        self.task19Entry.pack(fill = "x", padx = 29, pady = 5)
        self.task20Entry.pack(fill = "x", padx = 29, pady = 5)
        self.task21Entry.pack(fill = "x", padx = 29, pady = 5)

    def bind(self):
        pass

    def _updateEntry(self, entry:ttk.Entry, text:str):
        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, text)
        entry.config(state="readonly")

    @staticmethod
    def _formatAnswer(task_number, answer:list):
        ans = f"Задача {task_number} | "
        if len(answer) <= 6:
            ans += ' '.join(str(x) for x in answer)
        else:
            ans += ' '.join(str(x) for x in answer[:3]) + " ... " + ' '.join(str(x) for x in answer[-3:])
        ans += " | len = " + str(len(answer))
        ans += " | sum = " + str(sum(answer))
        return ans


class ViewManager:
    def __init__(self, solver:Solver):
        self.root = tk.Tk()
        self.inputFrame = ttk.Frame(self.root)
        self.configMainWindow()
        self.setStyles()
        self.actionsFrame = ActionsFrame(self.inputFrame, solver)
        self.heapsFrame = HeapsFrame(self.inputFrame, solver)
        self.answerFrame = AnswerFrame(self.root, solver)
        self.solver = solver

    def configMainWindow(self):
        self.root.title("Game theory solver")
        self.root.geometry("500x500")
        self.root.resizable(False, False)

    def setStyles(self):
        style = ttk.Style()
        style.configure("Custom.TFrame")
        style.configure("ActionListFrame.TFrame", background = "#DCE6FE")
        style.configure("Custom.TButton")
        style.configure("Custom.TEntry")
        style.configure("Custom.TLabel")

    def show(self):
        self.inputFrame.pack(expand = True, pady=(0,0))
        self.actionsFrame.show()
        self.heapsFrame.show()
        self.answerFrame.show()
    
    def bind(self):
        self.actionsFrame.bind()
        self.heapsFrame.bind()
        self.answerFrame.bind()
        self.answerFrame.solveButton.config(command=self.solve)

    def update(self):
        startCnt = self.heapsFrame.heapCntDistributionStartEntry.get()
        endCnt = self.heapsFrame.heapCntDistributionEndEntry.get()
        winCnt = self.heapsFrame.heapCntWinEntry.get()
        if self.solver._twoHeaps:
            otherHeap = self.heapsFrame.otherHeapCntEntry.get()
        try:
            startCnt = int(startCnt)
            endCnt = int(endCnt)
            winCnt = int(winCnt)
            if self.solver._twoHeaps:
                otherHeap = int(otherHeap)
        except:
            print("не число!")
            return
        
        try:
            self.solver.setWinCnt(winCnt)
            self.solver.setInterval(startCnt, endCnt)
            if self.solver._twoHeaps:
                self.solver.setOherHeapCnt(otherHeap)
        except:
            print("ошибка в установке значений")
        #print(self.solver._otherHeapCnt, self.solver._startCnt, self.solver._endCnt, self.solver._winCnt)

    def solve(self):
        self.update()
        task19, task20, task21 = self.solver.solve()
        print(task19, task20, task21)
        self.answerFrame._updateEntry(self.answerFrame.task19Entry, AnswerFrame._formatAnswer(19, task19))
        self.answerFrame._updateEntry(self.answerFrame.task20Entry, AnswerFrame._formatAnswer(20, task20))
        self.answerFrame._updateEntry(self.answerFrame.task21Entry, AnswerFrame._formatAnswer(21, task21))



class SolverApp:
    def __init__(self):
        self.solver = Solver()
        self.view = ViewManager(self.solver)
        self.bind()
    def run(self):
        self.view.show()
        tk.mainloop()
    def bind(self):
        self.view.bind()

app = SolverApp()
app.run()