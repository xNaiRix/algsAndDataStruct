import sys
import json
from dataclasses import asdict, dataclass
from typing import Optional, List, Dict, Callable
from itertools import permutations

from PySide6.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene,
                               QGraphicsItem, QGraphicsEllipseItem,
                               QGraphicsLineItem, QGraphicsTextItem,
                               QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QPushButton, QFileDialog, QMessageBox, QLabel,
                               QGroupBox, QRadioButton, QButtonGroup, QTextEdit,
                               QScrollArea)
from PySide6.QtCore import Qt, QRectF, QLineF, QPointF, Signal, QObject
from PySide6.QtGui import QPen, QBrush, QColor, QPainter, QPainterPathStroker, QAction

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
        print(event_type, data)
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
        self.events.subscribe("GraphStructUpdated", self._setGraphList)
        self.events.subscribe("GraphWeightUpdated", self._setGraphMatrix)
        self.events.subscribe("Func_changed", self._setFunc)
        self.events.subscribe("WaysTable_changeCell", self._setQuestionList)
        self.events.subscribe("SolveButton_click", self.solve)

    def _setVertCnt(self, data):
        new_cnt = int(data.get("entry", "0"))
        if new_cnt >= 0:
            self.vertCnt = new_cnt
            #print("solver:", self.vertCnt)

    def _setGraphList(self, data):
        #self.graphList = data["table"]
        self.graphList = data.values()
        print("solver:",self.graphList)

    def _setGraphMatrix(self, data):
        #self.graphMatrix = data["table"] - в ячейках строки
        self.graphMatrix = data
        print("solver:",self.graphMatrix)

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
        
    
# ==========================================
# 1. Configuration (Конфигурация)
# ==========================================
class GraphConfig:
    NODE_DIAMETER = 20  # Чуть больше, чтобы было виднее
    NODE_RADIUS = NODE_DIAMETER / 2
    EDGE_WIDTH = 2
    MIN_DISTANCE = 40

    COLOR_BG = QColor(40, 40, 40)
    COLOR_NODE = QColor(0, 255, 255)
    COLOR_NODE_ACTIVE = QColor(255, 0, 255)
    COLOR_EDGE = QColor(255, 255, 255)
    COLOR_TEXT = QColor(255, 255, 255)

    # Цвета для таблицы
    TABLE_BG = QColor(50, 50, 50)
    TABLE_TEXT = QColor(255, 255, 255)
    TABLE_DIAGONAL = QColor(80, 80, 80)  # Цвет диагонали


# ==========================================
# 2. Graph Visual Entities (Виджеты Графа)
# ==========================================
class EdgeItem(QGraphicsLineItem):
    def __init__(self, source_item, dest_item):
        super().__init__()
        self.source = source_item
        self.dest = dest_item
        self.setPen(QPen(GraphConfig.COLOR_EDGE, GraphConfig.EDGE_WIDTH))
        self.setZValue(0)
        self.update_geometry()

    def update_geometry(self):
        line = QLineF(self.source.scenePos(), self.dest.scenePos())
        self.setLine(line)

    def shape(self):
        path = super().shape()
        stroker = QPainterPathStroker()
        stroker.setWidth(10)
        return stroker.createStroke(path)


class NodeItem(QGraphicsEllipseItem):
    def __init__(self, name: str, x: float, y: float):
        rect = QRectF(-GraphConfig.NODE_RADIUS, -GraphConfig.NODE_RADIUS,
                      GraphConfig.NODE_DIAMETER, GraphConfig.NODE_DIAMETER)
        super().__init__(rect)
        self.name = name
        self.edges: List[EdgeItem] = []
        self.setBrush(QBrush(GraphConfig.COLOR_NODE))
        self.setPen(QPen(Qt.NoPen))
        self.setPos(x, y)
        self.setZValue(1)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self._create_label(name)

    def _create_label(self, text: str):
        self.label = QGraphicsTextItem(text, self)
        self.label.setDefaultTextColor(GraphConfig.COLOR_TEXT)
        # Центрируем текст относительно узла
        dx = -10 if len(text) == 1 else -15
        self.label.setPos(dx, -30)
        self.label.setFlag(QGraphicsItem.ItemIsMovable)
        self.label.setFlag(QGraphicsItem.ItemIgnoresTransformations)

    def set_highlighted(self, is_active: bool):
        color = GraphConfig.COLOR_NODE_ACTIVE if is_active else GraphConfig.COLOR_NODE
        self.setBrush(QBrush(color))

    def add_connection(self, edge: EdgeItem):
        self.edges.append(edge)

    def remove_connection(self, edge: EdgeItem):
        if edge in self.edges:
            self.edges.remove(edge)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged and self.scene():
            for edge in self.edges:
                edge.update_geometry()
        return super().itemChange(change, value)


# ==========================================
# 3. Graph Logic Managers
# ==========================================
class ChainBuilder:
    def __init__(self):
        self.active_node: Optional[NodeItem] = None

    def start_or_continue(self, node: NodeItem) -> Optional[NodeItem]:
        prev_node = self.active_node
        if self.active_node:
            self.active_node.set_highlighted(False)
        self.active_node = node
        self.active_node.set_highlighted(True)
        return prev_node

    def reset(self):
        if self.active_node:
            self.active_node.set_highlighted(False)
            self.active_node = None


class GraphManager(QObject):
    # Сигнал об изменении количества узлов (для таблицы)
    node_count_changed = Signal(int)

    def __init__(self, scene: QGraphicsScene, eventManager:EventManager):
        super().__init__()
        self.scene = scene
        self.node_counter = 0
        self.eventManager = eventManager

        self.eventManager.publish("GraphStructUpdated", self.get_adjacency_list())

    def reset(self):
        self.node_counter = 0
        self.scene.clear()
        self.node_count_changed.emit(0)

        self.eventManager.publish("GraphStructUpdated", self.get_adjacency_list())

    def generate_name(self) -> str:
        n = self.node_counter
        name = ""
        while n >= 0:
            name = chr(ord('A') + (n % 26)) + name
            n = n // 26 - 1
        self.node_counter += 1
        
        return name

    def create_node(self, pos: QPointF, name: str = None) -> NodeItem:
        if name is None:
            name = self.generate_name()
        else:
            # Если загружаем из файла, нужно обновить счетчик, чтобы новые имена не конфликтовали
            # Простая эвристика: увеличиваем счетчик
            self.node_counter += 1

        node = NodeItem(name, pos.x(), pos.y())
        self.scene.addItem(node)
        self.node_count_changed.emit(self.get_node_count())

        self.eventManager.publish("GraphStructUpdated", self.get_adjacency_list())

        return node

    def create_edge(self, u: NodeItem, v: NodeItem):
        if u == v: return
        # Проверка дубликатов
        for edge in u.edges:
            if (edge.source == u and edge.dest == v) or (edge.source == v and edge.dest == u):
                return
        edge = EdgeItem(u, v)
        self.scene.addItem(edge)
        u.add_connection(edge)
        v.add_connection(edge)
        
        self.eventManager.publish("GraphStructUpdated", self.get_adjacency_list())

    def delete_item(self, item: QGraphicsItem):
        if isinstance(item, NodeItem):
            for edge in list(item.edges):
                self.delete_item(edge)
            self.scene.removeItem(item)
            self.node_count_changed.emit(self.get_node_count())
        elif isinstance(item, EdgeItem):
            item.source.remove_connection(item)
            item.dest.remove_connection(item)
            self.scene.removeItem(item)
        elif isinstance(item, QGraphicsTextItem):
            parent = item.parentItem()
            if isinstance(parent, NodeItem):
                self.delete_item(parent)

        self.eventManager.publish("GraphStructUpdated", self.get_adjacency_list())

    def get_node_count(self) -> int:
        return sum(1 for item in self.scene.items() if isinstance(item, NodeItem))

    def is_position_valid(self, pos: QPointF) -> bool:
        for item in self.scene.items():
            if isinstance(item, NodeItem):
                distance = QLineF(pos, item.scenePos()).length()
                if distance < GraphConfig.MIN_DISTANCE:
                    return False
        return True
    ####
    
    def get_adjacency_list(self) -> Dict[str, List[str]]:
        """
        Возвращает список смежности в формате:
        {'A': ['B', 'C'], 'B': ['A'], 'C': ['A']}
        """
        adj_list = {}
        
        # Собираем все узлы
        nodes = [item for item in self.scene.items() if isinstance(item, NodeItem)]
        
        # Инициализируем пустые списки для каждого узла
        for node in nodes:
            adj_list[node.name] = []
        
        # Заполняем списки смежности
        for node in nodes:
            for edge in node.edges:
                # Определяем соседний узел
                if edge.source == node:
                    neighbor = edge.dest
                else:
                    neighbor = edge.source
                
                # Добавляем в список смежности (без дубликатов)
                if neighbor.name not in adj_list[node.name]:
                    adj_list[node.name].append(neighbor.name)
        
        return adj_list


# ==========================================
# 4.1. Ways Table Widget (Таблица путей)
# ==========================================
class WaysTableWidget(QWidget):
    def __init__(self, eventManager: EventManager):
        super().__init__()
        self.eventManager = eventManager
        self.initial_state = [["", ""]]  # Изначально одна пустая строка
        
        self.init_ui()
        self.reset_table()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("Таблица путей")
        layout.addWidget(title)
        
        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["от", "до"])
        
        # Стилизация таблицы
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {GraphConfig.TABLE_BG.name()};
                color: {GraphConfig.TABLE_TEXT.name()};
                gridline-color: #666;
            }}
            QHeaderView::section {{
                background-color: #333;
                color: white;
                padding: 4px;
                border: 1px solid #666;
            }}
        """)
        
        # Настройка ширины столбцов
        self.table.horizontalHeader().setDefaultSectionSize(60)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        
        # Обработка изменений
        self.table.itemChanged.connect(self.on_item_changed)
        
        layout.addWidget(self.table)
        
        # Кнопки
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_row)
        
        self.reset_button = QPushButton("Сбросить")
        self.reset_button.clicked.connect(self.reset_table)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.reset_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def add_row(self):
        """Добавляет пустую строку в начало таблицы"""
        current_rows = self.table.rowCount()
        self.table.insertRow(0)
        
        # Создаем пустые ячейки
        for col in range(2):
            item = QTableWidgetItem("")
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(0, col, item)
        
        self.publish_current_state()
    
    def reset_table(self):
        """Возвращает таблицу к исходному состоянию"""
        self.table.blockSignals(True)
        
        self.table.setRowCount(len(self.initial_state))
        for row, row_data in enumerate(self.initial_state):
            for col, cell_data in enumerate(row_data):
                item = QTableWidgetItem(cell_data)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)
        
        self.table.blockSignals(False)
        self.publish_current_state()
    
    def on_item_changed(self, item):
        """Обрабатывает изменение ячейки"""
        self.publish_current_state()
    
    def publish_current_state(self):
        """Публикует текущее состояние таблицы"""
        data = self.get_data()
        self.eventManager.publish("WaysTable_changeCell", {"table": data})
    
    def get_data(self) -> List[List[str]]:
        """Возвращает текущие данные таблицы"""
        rows = self.table.rowCount()
        data = []
        for row in range(rows):
            row_data = []
            for col in range(2):
                item = self.table.item(row, col)
                row_data.append(item.text() if item else "")
            data.append(row_data)
        return data


# ==========================================
# 4.2. Function Selector Widget (Выбор функции)
# ==========================================
class FunctionSelectorWidget(QWidget):
    def __init__(self, eventManager: EventManager):
        super().__init__()
        self.eventManager = eventManager
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("Функция")
        layout.addWidget(title)
        
        # Группа радиокнопок
        self.radio_sum = QRadioButton("sum")
        self.radio_min = QRadioButton("min") 
        self.radio_max = QRadioButton("max")
        
        # Группируем радиокнопки
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.radio_sum)
        self.button_group.addButton(self.radio_min)
        self.button_group.addButton(self.radio_max)
        
        # Устанавливаем sum по умолчанию
        self.radio_sum.setChecked(True)
        
        # Стилизация радиокнопок
        radio_style = f"""
            QRadioButton {{
                color: {GraphConfig.COLOR_TEXT.name()};
                spacing: 5px;
            }}
            QRadioButton::indicator {{
                width: 12px;
                height: 12px;
            }}
            QRadioButton::indicator:unchecked {{
                border: 2px solid #666;
                border-radius: 6px;
                background-color: {GraphConfig.TABLE_BG.name()};
            }}
            QRadioButton::indicator:checked {{
                border: 2px solid #00FFFF;
                border-radius: 6px;
                background-color: #00FFFF;
            }}
        """
        self.radio_sum.setStyleSheet(radio_style)
        self.radio_min.setStyleSheet(radio_style)
        self.radio_max.setStyleSheet(radio_style)
        
        # Добавляем в layout
        layout.addWidget(self.radio_sum)
        layout.addWidget(self.radio_min)
        layout.addWidget(self.radio_max)
        
        # Кнопка "Решить"
        self.solve_button = QPushButton("Решить")
        self.solve_button.clicked.connect(self.on_solve_clicked)
        
        # Стилизация кнопки
        self.solve_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #00FFFF;
                color: black;
                font-weight: bold;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: #00E5E5;
            }}
            QPushButton:pressed {{
                background-color: #00CCCC;
            }}
        """)
        
        layout.addWidget(self.solve_button)
        
        # Обработка изменений
        self.button_group.buttonClicked.connect(self.on_function_changed)
        
        # Добавляем растягивающийся элемент для выравнивания
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Публикуем начальное значение
        self.publish_function()
    
    def on_function_changed(self, button):
        """Обрабатывает изменение выбранной функции"""
        self.publish_function()
    
    def on_solve_clicked(self):
        """Обрабатывает нажатие кнопки 'Решить'"""
        self.eventManager.publish("SolveButton_click", {})
    
    def publish_function(self):
        """Публикует выбранную функцию"""
        if self.radio_sum.isChecked():
            func = "sum"
        elif self.radio_min.isChecked():
            func = "min"
        else:  # self.radio_max.isChecked()
            func = "max"
            
        self.eventManager.publish("Func_changed", {"func": func})


# ==========================================
# 4.3. Result Display Widget (Отображение результатов)
# ==========================================
class ResultDisplayWidget(QWidget):
    def __init__(self, eventManager: EventManager):
        super().__init__()
        self.eventManager = eventManager
        self.init_ui()
        self.eventManager.subscribe("solveEnded", self.on_solve_ended)
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("Результаты")
        layout.addWidget(title)
        
        # Текстовое поле для ответа
        answer_layout = QVBoxLayout()
        answer_label = QLabel("Ответ:")
        self.answer_text = QTextEdit()
        self.answer_text.setReadOnly(True)
        self.answer_text.setMaximumHeight(60)
        self.answer_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {GraphConfig.TABLE_BG.name()};
                color: {GraphConfig.COLOR_TEXT.name()};
                border: 1px solid #666;
                padding: 5px;
            }}
        """)
        answer_layout.addWidget(answer_label)
        answer_layout.addWidget(self.answer_text)
        
        # Таблица соответствия букв-цифр
        table_layout = QVBoxLayout()
        table_label = QLabel("Соответствие:")
        self.mapping_table = QTableWidget()
        self.mapping_table.setRowCount(1)  # Одна строка с буквами
        self.mapping_table.verticalHeader().setVisible(False)  # Скрываем подписи строк
        self.mapping_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {GraphConfig.TABLE_BG.name()};
                color: {GraphConfig.COLOR_TEXT.name()};
                gridline-color: #666;
            }}
            QHeaderView::section {{
                background-color: #333;
                color: white;
                padding: 4px;
                border: 1px solid #666;
            }}
        """)
        
        # Настройка таблицы
        self.mapping_table.horizontalHeader().setDefaultSectionSize(40)
        self.mapping_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.mapping_table.setSelectionMode(QTableWidget.SingleSelection)
        self.mapping_table.setSelectionBehavior(QTableWidget.SelectItems)
        
        table_layout.addWidget(table_label)
        table_layout.addWidget(self.mapping_table)
        
        layout.addLayout(answer_layout)
        layout.addLayout(table_layout)
        
        self.setLayout(layout)
    
    def on_solve_ended(self, data):
        """Обрабатывает событие завершения решения"""
        answer = data.get("answer", "")
        table = data.get("table", {})
        
        # Обновляем текстовое поле с ответом
        self.answer_text.setText(answer)
        
        # Обновляем таблицу соответствия
        self.update_mapping_table(table)
    
    def update_mapping_table(self, table_dict):
        """Обновляет таблицу соответствия букв-цифр"""
        if not table_dict:
            self.mapping_table.setColumnCount(0)
            return
        
        # Сортируем ключи (цифры) для правильного порядка столбцов
        sorted_keys = sorted(table_dict.keys(), key=lambda x: int(x))
        column_count = len(sorted_keys)
        
        # Устанавливаем количество столбцов
        self.mapping_table.setColumnCount(column_count)
        
        # Устанавливаем заголовки столбцов (цифры)
        self.mapping_table.setHorizontalHeaderLabels(sorted_keys)
        
        # Заполняем ячейки буквами
        for col, key in enumerate(sorted_keys):
            letter = table_dict[key]
            item = QTableWidgetItem(letter)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)  # Только чтение, но можно выделять
            self.mapping_table.setItem(0, col, item)


# ==========================================
# 4.4. Matrix Widget (Таблица весов)
# ==========================================
class WeightMatrixWidget(QTableWidget):
    def __init__(self, eventManager:EventManager):
        super().__init__()
        self.setColumnCount(0)
        self.setRowCount(0)
        self.setWindowTitle("Матрица весов")
        self.eventManager = eventManager

        # Стилизация таблицы под темную тему
        self.setStyleSheet(f"""
            QTableWidget {{
                background-color: {GraphConfig.TABLE_BG.name()};
                color: {GraphConfig.TABLE_TEXT.name()};
                gridline-color: #666;
            }}
            QHeaderView::section {{
                background-color: #333;
                color: white;
                padding: 4px;
                border: 1px solid #666;
            }}
            QLineEdit {{ color: white; background-color: #444; }}
        """)

        # Обработка изменений для симметрии
        self.itemChanged.connect(self.on_item_changed)

        # Настраиваем адаптивный размер ячеек
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        
        self.eventManager.publish("GraphWeightUpdated", self.get_data())
        
    def calculate_cell_size(self, node_count: int) -> int:
        """Рассчитывает оптимальный размер ячейки в зависимости от количества узлов"""
        if node_count <= 4:
            return 60  # Большие ячейки для маленьких матриц
        elif node_count <= 6:
            return 50
        elif node_count <= 8:
            return 40
        elif node_count <= 12:
            return 35
        else:
            return 30  # Минимальный размер для больших матриц

    def update_size(self, node_count: int):
        """Обновляет размер таблицы при добавлении/удалении узлов графа"""
        current_rows = self.rowCount()

        self.setRowCount(node_count)
        self.setColumnCount(node_count)

        headers = [str(i + 1) for i in range(node_count)]
        self.setHorizontalHeaderLabels(headers)
        self.setVerticalHeaderLabels(headers)

        # Рассчитываем оптимальный размер ячеек
        cell_size = self.calculate_cell_size(node_count)
        self.horizontalHeader().setDefaultSectionSize(cell_size)
        self.verticalHeader().setDefaultSectionSize(cell_size)

        # Блокировка сигналов во время перестройки, чтобы не триггерить on_item_changed
        self.blockSignals(True)

        # Настройка ячеек (диагональ и пустые)
        for r in range(node_count):
            for c in range(node_count):
                item = self.item(r, c)
                if not item:
                    item = QTableWidgetItem("")
                    item.setTextAlignment(Qt.AlignCenter)
                    self.setItem(r, c, item)

                # Диагональ
                if r == c:
                    item.setFlags(Qt.ItemIsEnabled)  # Только чтение
                    item.setBackground(QBrush(GraphConfig.TABLE_DIAGONAL))
                else:
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                    item.setBackground(QBrush(GraphConfig.TABLE_BG))

        self.blockSignals(False)
        self.eventManager.publish("GraphWeightUpdated", self.get_data())

    def on_item_changed(self, item):
        """Обеспечивает симметричность матрицы"""
        row = item.row()
        col = item.column()

        if row == col: return

        text = item.text()

        # Блокируем сигналы, чтобы не уйти в бесконечную рекурсию
        self.blockSignals(True)

        symmetric_item = self.item(col, row)
        if symmetric_item:
            symmetric_item.setText(text)

        self.blockSignals(False)
        self.eventManager.publish("GraphWeightUpdated", self.get_data())

    def get_data(self) -> List[List[str]]:
        rows = self.rowCount()
        data = []
        for r in range(rows):
            row_data = []
            for c in range(rows):
                item = self.item(r, c)
                row_data.append(item.text() if item else "")
            data.append(row_data)

        return data

    def set_data(self, data: List[List[str]]):
        size = len(data)
        self.update_size(size)
        self.blockSignals(True)
        for r in range(size):
            for c in range(size):
                if r < len(data) and c < len(data[r]):
                    val = data[r][c]
                    item = self.item(r, c)
                    if item:
                        item.setText(val)
        self.blockSignals(False)
        self.eventManager.publish("GraphWeightUpdated", self.get_data())


# ==========================================
# 5. Graph Scene & View
# ==========================================
class GraphScene(QGraphicsScene):
    def __init__(self, manager: GraphManager, parent=None):
        super().__init__(parent)
        self.manager = manager
        self.chain_builder = ChainBuilder()
        self.setBackgroundBrush(QBrush(GraphConfig.COLOR_BG))
        self.setSceneRect(0, 0, 800, 600)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.chain_builder.reset()
        super().keyReleaseEvent(event)

    def mousePressEvent(self, event):
        pos = event.scenePos()
        item = self.itemAt(pos, self.views()[0].transform())

        if event.button() == Qt.LeftButton:
            if event.modifiers() & Qt.ShiftModifier:
                if isinstance(item, NodeItem):
                    prev_node = self.chain_builder.start_or_continue(item)
                    if prev_node:
                        self.manager.create_edge(prev_node, item)
                    event.accept()
                    return
                else:
                    self.chain_builder.reset()
            else:
                self.chain_builder.reset()

            if item is None:
                if self.manager.is_position_valid(pos):
                    self.manager.create_node(pos)
                event.accept()
                return

            super().mousePressEvent(event)

        elif event.button() == Qt.RightButton:
            self.chain_builder.reset()
            if item:
                self.manager.delete_item(item)
                event.accept()


# ==========================================
# 6. Main Application Window
# ==========================================
class MainWindow(QMainWindow):
    def __init__(self, event_manager:EventManager):
        super().__init__()
        self.setWindowTitle("Тренажер: Граф и Матрица весов (ЕГЭ Информатика)")
        self.resize(1400, 800)  # Увеличил размер окна для лучшего отображения

        # 1. Сцена и Менеджер
        self.scene = QGraphicsScene()  # Placeholder initialization
        self.event_manager = event_manager
        self.graph_manager = GraphManager(self.scene, self.event_manager)
        self.scene = GraphScene(self.graph_manager, self)  # Override with custom scene
        self.graph_manager.scene = self.scene  # Re-link

        # 2. Виджеты
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)

        self.matrix_widget = WeightMatrixWidget(self.event_manager)
        self.ways_widget = WaysTableWidget(self.event_manager)
        self.function_selector = FunctionSelectorWidget(self.event_manager)
        self.result_display = ResultDisplayWidget(self.event_manager)

        # 3. Связь Граф -> Таблица
        self.graph_manager.node_count_changed.connect(self.matrix_widget.update_size)

        # 4. Лейаут
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)

        # Левая часть (Матрица, пути, функция и результаты)
        left_layout = QVBoxLayout()
        
        # Группа для матрицы весов с возможностью прокрутки
        matrix_group = QGroupBox("Матрица весов")
        matrix_layout = QVBoxLayout()
        
        # Создаем область прокрутки для матрицы
        matrix_scroll = QScrollArea()
        matrix_scroll.setWidgetResizable(True)
        matrix_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        matrix_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        matrix_scroll.setWidget(self.matrix_widget)
        matrix_scroll.setMinimumHeight(200)  # Минимальная высота для отображения
        matrix_scroll.setMaximumHeight(600)  # Максимальная высота
        
        matrix_layout.addWidget(matrix_scroll)
        matrix_group.setLayout(matrix_layout)
        
        # Группа для таблицы путей и функции
        ways_function_layout = QHBoxLayout()
        
        # Таблица путей
        ways_group = QGroupBox("Таблица путей")
        ways_group_layout = QVBoxLayout()
        ways_group_layout.addWidget(self.ways_widget)
        ways_group.setLayout(ways_group_layout)
        
        # Выбор функции и кнопка решения
        function_group = QGroupBox("Функция")
        function_group_layout = QVBoxLayout()
        function_group_layout.addWidget(self.function_selector)
        function_group.setLayout(function_group_layout)
        
        ways_function_layout.addWidget(ways_group)
        ways_function_layout.addWidget(function_group)
        
        # Группа для результатов
        results_group = QGroupBox("Результаты")
        results_layout = QVBoxLayout()
        results_layout.addWidget(self.result_display)
        results_group.setLayout(results_layout)
        
        left_layout.addWidget(matrix_group, 2)  # Больше места для матрицы
        left_layout.addLayout(ways_function_layout, 1)
        left_layout.addWidget(results_group, 1)

        # Правая часть (Граф)
        right_layout = QVBoxLayout()
        right_label = QLabel("Редактор графа (ЛКМ - узел, Shift+ЛКМ - ребро, ПКМ - удалить)")
        right_layout.addWidget(right_label)
        right_layout.addWidget(self.view)

        main_layout.addLayout(left_layout, 1)  # stretch factor 1
        main_layout.addLayout(right_layout, 2)  # stretch factor 2 (граф шире)

        self.setCentralWidget(central_widget)

        # 5. Меню
        self.create_menu()

    def create_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu("Файл")

        save_action = QAction("Сохранить упражнение...", self)
        save_action.triggered.connect(self.save_exercise)
        file_menu.addAction(save_action)

        load_action = QAction("Загрузить упражнение...", self)
        load_action.triggered.connect(self.load_exercise)
        file_menu.addAction(load_action)

        clear_action = QAction("Очистить всё", self)
        clear_action.triggered.connect(self.clear_all)
        file_menu.addAction(clear_action)

    def clear_all(self):
        self.graph_manager.reset()
        self.matrix_widget.update_size(0)

    def save_exercise(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "JSON Files (*.json)")
        if not file_path:
            return

        # Сбор данных графа
        nodes_data = []
        node_id_map = {}  # Object -> ID

        # Находим все узлы
        items = [i for i in self.scene.items() if isinstance(i, NodeItem)]
        # Сортируем по имени, чтобы порядок был детерминированным (опционально)
        # Но нам важнее просто назначить ID
        for idx, node in enumerate(items):
            node_id_map[node] = idx
            nodes_data.append({
                "id": idx,
                "name": node.name,
                "x": node.pos().x(),
                "y": node.pos().y()
            })

        edges_data = []
        visited_edges = set()
        for node in items:
            for edge in node.edges:
                if edge not in visited_edges:
                    visited_edges.add(edge)
                    u_id = node_id_map.get(edge.source)
                    v_id = node_id_map.get(edge.dest)
                    if u_id is not None and v_id is not None:
                        edges_data.append({"u": u_id, "v": v_id})

        # Сбор данных матрицы
        matrix_data = self.matrix_widget.get_data()
        ways_data = self.ways_widget.get_data()
        
        # Определяем выбранную функцию
        if self.function_selector.radio_sum.isChecked():
            func = "sum"
        elif self.function_selector.radio_min.isChecked():
            func = "min"
        else:
            func = "max"
        
        data = {
            "graph": {
                "nodes": nodes_data,
                "edges": edges_data,
                "node_counter": self.graph_manager.node_counter
            },
            "matrix": matrix_data,
            "ways": ways_data,
            "function": func
        }

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Успех", "Упражнение сохранено!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить: {e}")

    def load_exercise(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "JSON Files (*.json)")
        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 1. Очистка
            self.clear_all()

            # 2. Восстановление графа
            graph_data = data.get("graph", {})
            nodes_list = graph_data.get("nodes", [])
            edges_list = graph_data.get("edges", [])

            # Восстанавливаем счетчик имен
            self.graph_manager.node_counter = graph_data.get("node_counter", 0)

            # Создаем узлы и мапим ID -> NodeItem
            id_to_node = {}
            for n_data in nodes_list:
                pos = QPointF(n_data["x"], n_data["y"])
                name = n_data["name"]
                node = self.graph_manager.create_node(pos, name)
                id_to_node[n_data["id"]] = node

            # Создаем ребра
            for e_data in edges_list:
                u = id_to_node.get(e_data["u"])
                v = id_to_node.get(e_data["v"])
                if u and v:
                    self.graph_manager.create_edge(u, v)

            # 3. Восстановление матрицы
            matrix_data = data.get("matrix", [])
            self.matrix_widget.set_data(matrix_data)
            
            # 4. Восстановление таблицы путей
            ways_data = data.get("ways", [["", ""]])
            self.ways_widget.table.blockSignals(True)
            self.ways_widget.table.setRowCount(len(ways_data))
            for row, row_data in enumerate(ways_data):
                for col, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(cell_data)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ways_widget.table.setItem(row, col, item)
            self.ways_widget.table.blockSignals(False)
            self.ways_widget.publish_current_state()
            
            # 5. Восстановление функции
            func = data.get("function", "sum")
            if func == "min":
                self.function_selector.radio_min.setChecked(True)
            elif func == "max":
                self.function_selector.radio_max.setChecked(True)
            else:
                self.function_selector.radio_sum.setChecked(True)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Установка темной темы для всего приложения
    app.setStyle("Fusion")
    palette = app.palette()
    palette.setColor(palette.ColorRole.Window, QColor(53, 53, 53))
    palette.setColor(palette.ColorRole.WindowText, Qt.white)
    palette.setColor(palette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(palette.ColorRole.AlternateBase, QColor(53, 53, 53))
    palette.setColor(palette.ColorRole.ToolTipBase, Qt.white)
    palette.setColor(palette.ColorRole.ToolTipText, Qt.white)
    palette.setColor(palette.ColorRole.Text, Qt.white)
    palette.setColor(palette.ColorRole.Button, QColor(53, 53, 53))
    palette.setColor(palette.ColorRole.ButtonText, Qt.white)
    palette.setColor(palette.ColorRole.BrightText, Qt.red)
    palette.setColor(palette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(palette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(palette.ColorRole.HighlightedText, Qt.black)
    app.setPalette(palette)

    event_manager = EventManager()
    window = MainWindow(event_manager)
    solver = Solver(event_manager)
    window.show()
    sys.exit(app.exec())