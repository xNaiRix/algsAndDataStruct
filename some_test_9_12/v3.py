import sys
import json
import time
from enum import Enum
from datetime import datetime
from typing import List, Dict, Any, Optional

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QPushButton, QLabel, QFileDialog,
                               QStackedWidget, QMessageBox, QRadioButton,
                               QCheckBox, QButtonGroup, QLineEdit, QPlainTextEdit,
                               QListWidget, QListWidgetItem, QAbstractItemView,
                               QScrollArea, QTextBrowser, QFrame, QGridLayout, QSizePolicy)
from PySide6.QtCore import Qt, QTimer, Signal, QSize, QEvent
from PySide6.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor, QPalette


# ==========================================
# 1. Утилиты: Подсветка синтаксиса Python
# ==========================================

class PythonHighlighter(QSyntaxHighlighter):
    """Простой подсветчик синтаксиса для Python кода."""

    def __init__(self, document):
        super().__init__(document)
        self.highlightingRules = []

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor("#569CD6") if True else Qt.darkBlue)  # Light blue for dark theme mostly
        keywordFormat.setFontWeight(QFont.Bold)
        keywords = ["def", "class", "if", "else", "elif", "while", "for", "return",
                    "import", "from", "print", "try", "except", "in", "and", "or", "not", "pass"]
        for pattern in keywords:
            self.highlightingRules.append((r"\b" + pattern + r"\b", keywordFormat))

        stringFormat = QTextCharFormat()
        stringFormat.setForeground(QColor("#CE9178"))  # Orange-ish for strings
        self.highlightingRules.append((r"\".*\"", stringFormat))
        self.highlightingRules.append((r"'.*'", stringFormat))

        commentFormat = QTextCharFormat()
        commentFormat.setForeground(QColor("#6A9955"))  # Green for comments
        self.highlightingRules.append((r"#[^\n]*", commentFormat))

    def highlightBlock(self, text):
        import re
        for pattern, format in self.highlightingRules:
            expression = re.compile(pattern)
            matches = expression.finditer(text)
            for match in matches:
                self.setFormat(match.start(), match.end() - match.start(), format)


# ==========================================
# 2. Модели данных
# ==========================================

class QuestionType(str, Enum):
    SINGLE_CHOICE = "single_choice"
    MULTI_CHOICE = "multi_choice"
    INPUT = "input"
    ORDERING = "ordering"
    CODE = "code"
    CODE_FRAGMENT = "code_fragment"


class ExerciseModel:
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get("id")
        self.type = QuestionType(data.get("type"))
        self.question_html = data.get("question", "")
        self.options = data.get("options", [])

        # Для обычного кода и фрагментов
        self.initial_code = data.get("initial_code", "")

        # Специфично для code_fragment
        self.prefix = data.get("prefix", "")
        self.suffix = data.get("suffix", "")


class TestSession:
    def __init__(self):
        self.start_time = datetime.now().isoformat()
        self.events = []
        self.answers = {}

    def log_event(self, action: str, exercise_id: Any = None, payload: Any = None):
        event = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "exercise_id": exercise_id,
            "payload": payload
        }
        self.events.append(event)

    def record_answer(self, exercise_id, answer):
        self.answers[exercise_id] = answer
        self.log_event("answer_update", exercise_id, answer)

    def has_answer(self, exercise_id):
        # Проверка, есть ли непустой ответ
        ans = self.answers.get(exercise_id)
        if ans is None: return False
        if isinstance(ans, str) and ans.strip() == "": return False
        if isinstance(ans, list) and len(ans) == 0: return False
        return True

    def export_json(self):
        return json.dumps({
            "meta": {
                "start_time": self.start_time,
                "end_time": datetime.now().isoformat()
            },
            "answers": self.answers,
            "log": self.events
        }, indent=4, ensure_ascii=False)


class RestrictedCodeEditor(QPlainTextEdit):
    """
    Редактор кода, который разрешает менять текст только между prefix и suffix.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.prefix = ""
        self.suffix = ""
        font = QFont("Courier New")
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)

    def set_parts(self, prefix, editable, suffix):
        self.prefix = prefix
        self.suffix = suffix
        # Устанавливаем полный текст
        self.setPlainText(prefix + editable + suffix)

    def keyPressEvent(self, event):
        cursor = self.textCursor()
        position = cursor.position()
        document_len = self.document().characterCount() - 1  # -1 т.к. есть невидимый символ конца

        # Границы редактируемой зоны
        editable_start = len(self.prefix)
        editable_end = document_len - len(self.suffix)

        # Разрешаем навигацию (стрелки, home, end)
        if event.key() in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down,
                           Qt.Key_Home, Qt.Key_End, Qt.Key_PageUp, Qt.Key_PageDown):
            super().keyPressEvent(event)
            return

        # Проверка на выделение: если выделение задевает запретные зоны - блокируем
        if cursor.hasSelection():
            sel_start = cursor.selectionStart()
            sel_end = cursor.selectionEnd()
            if sel_start < editable_start or sel_end > editable_end:
                return  # Запрещаем удалять/заменять защищенный текст

        # Обработка Backspace
        if event.key() == Qt.Key_Backspace:
            if position <= editable_start:
                return  # Нельзя стирать префикс

        # Обработка Delete
        elif event.key() == Qt.Key_Delete:
            if position >= editable_end:
                return  # Нельзя стирать суффикс

        # Обычный ввод текста
        else:
            # Если текст (не управляющая клавиша типа Ctrl)
            if event.text():
                # Если курсор вне зоны редактирования
                if position < editable_start:
                    cursor.setPosition(editable_start)
                    self.setTextCursor(cursor)
                elif position > editable_end:
                    cursor.setPosition(editable_end)
                    self.setTextCursor(cursor)

        super().keyPressEvent(event)

    def get_editable_part(self):
        full_text = self.toPlainText()
        # Вырезаем середину
        if full_text.startswith(self.prefix) and full_text.endswith(self.suffix):
            return full_text[len(self.prefix): len(full_text) - len(self.suffix)]
        return full_text  # Fallback

# ==========================================
# 3. Виджеты упражнений
# ==========================================

class BaseExerciseWidget(QWidget):
    answerChanged = Signal(object)

    def __init__(self, model: ExerciseModel):
        super().__init__()
        self.model = model
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Задание
        self.question_browser = QTextBrowser()
        self.question_browser.setHtml(self.model.question_html)
        self.question_browser.setOpenExternalLinks(False)
        self.question_browser.setMaximumHeight(250)
        layout.addWidget(self.question_browser)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        layout.addWidget(line)

        # Зона ответа
        self.answer_area = QWidget()
        self.answer_layout = QVBoxLayout(self.answer_area)
        self.create_answer_widgets()
        layout.addWidget(self.answer_area)

        layout.addStretch()

    def create_answer_widgets(self):
        pass

    def get_answer(self):
        raise NotImplementedError


class SingleChoiceWidget(BaseExerciseWidget):
    def create_answer_widgets(self):
        self.button_group = QButtonGroup(self)
        self.button_group.buttonClicked.connect(lambda: self.answerChanged.emit(self.get_answer()))

        for idx, option in enumerate(self.model.options):
            rb = QRadioButton(option)
            self.answer_layout.addWidget(rb)
            self.button_group.addButton(rb, idx)

    def get_answer(self):
        btn = self.button_group.checkedButton()
        if btn:
            return self.button_group.id(btn)
        return None


class MultiChoiceWidget(BaseExerciseWidget):
    def create_answer_widgets(self):
        self.checkboxes = []
        for option in self.model.options:
            cb = QCheckBox(option)
            cb.stateChanged.connect(lambda: self.answerChanged.emit(self.get_answer()))
            self.answer_layout.addWidget(cb)
            self.checkboxes.append(cb)

    def get_answer(self):
        return [i for i, cb in enumerate(self.checkboxes) if cb.isChecked()]


class InputWidget(BaseExerciseWidget):
    def create_answer_widgets(self):
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ответ...")
        self.input_field.textChanged.connect(lambda: self.answerChanged.emit(self.get_answer()))
        self.answer_layout.addWidget(self.input_field)

    def get_answer(self):
        return self.input_field.text()


class OrderingWidget(BaseExerciseWidget):
    def create_answer_widgets(self):
        label = QLabel("Перетащите элементы:")
        self.answer_layout.addWidget(label)
        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QAbstractItemView.InternalMove)
        self.list_widget.model().rowsMoved.connect(lambda: self.answerChanged.emit(self.get_answer()))
        for option in self.model.options:
            item = QListWidgetItem(option)
            self.list_widget.addItem(item)
        self.answer_layout.addWidget(self.list_widget)

    def get_answer(self):
        return [self.list_widget.item(i).text() for i in range(self.list_widget.count())]


class CodeWidget(BaseExerciseWidget):
    def create_answer_widgets(self):
        self.editor = QPlainTextEdit()
        font = QFont("Courier New")
        font.setStyleHint(QFont.Monospace)
        self.editor.setFont(font)
        self.highlighter = PythonHighlighter(self.editor.document())
        if self.model.initial_code:
            self.editor.setPlainText(self.model.initial_code)
        self.editor.textChanged.connect(lambda: self.answerChanged.emit(self.get_answer()))
        self.answer_layout.addWidget(self.editor)

    def get_answer(self):
        return self.editor.toPlainText()


class CodeFragmentWidget(BaseExerciseWidget):
    def create_answer_widgets(self):
        # Кнопка сброса
        btn_layout = QHBoxLayout()
        self.btn_reset = QPushButton("Вернуть условие")
        self.btn_reset.setFixedWidth(150)
        self.btn_reset.clicked.connect(self.reset_code)
        btn_layout.addWidget(self.btn_reset)
        btn_layout.addStretch()
        self.answer_layout.addLayout(btn_layout)

        # Редактор
        self.editor = RestrictedCodeEditor()
        self.highlighter = PythonHighlighter(self.editor.document())

        # Инициализация
        self.reset_code()

        self.editor.textChanged.connect(lambda: self.answerChanged.emit(self.get_answer()))
        self.answer_layout.addWidget(self.editor)

    def reset_code(self):
        self.editor.set_parts(self.model.prefix, self.model.initial_code, self.model.suffix)
        self.answerChanged.emit(self.model.initial_code)

    def get_answer(self):
        return self.editor.get_editable_part()


class WidgetFactory:
    @staticmethod
    def create_widget(model: ExerciseModel) -> BaseExerciseWidget:
        if model.type == QuestionType.SINGLE_CHOICE:
            return SingleChoiceWidget(model)
        elif model.type == QuestionType.MULTI_CHOICE:
            return MultiChoiceWidget(model)
        elif model.type == QuestionType.INPUT:
            return InputWidget(model)
        elif model.type == QuestionType.ORDERING:
            return OrderingWidget(model)
        elif model.type == QuestionType.CODE:
            return CodeWidget(model)
        elif model.type == QuestionType.CODE_FRAGMENT:  # <--- Добавлено
            return CodeFragmentWidget(model)
        else:
            return BaseExerciseWidget(model)


# ==========================================
# 4. Компоненты навигации
# ==========================================

class NavButton(QPushButton):
    """Кнопка навигации в левой панели (квадратик)."""

    def __init__(self, index, parent=None):
        super().__init__(str(index + 1), parent)
        self.index = index
        self.is_current = False
        self.has_answer = False
        self.setFixedSize(40, 40)
        self.setCursor(Qt.PointingHandCursor)
        self.update_style()

    def set_state(self, is_current, has_answer):
        self.is_current = is_current
        self.has_answer = has_answer
        self.update_style()

    def update_style(self):
        # Базовые цвета, совместимые с темной темой
        border_color = "#888888"
        bg_color = "transparent"
        text_color = "palette(text)"

        # Если есть ответ - заливка
        if self.has_answer:
            bg_color = "#555555"  # Серый фон для решенных
            border_color = "#555555"

        # Если текущий - яркая рамка
        border_style = f"1px solid {border_color}"
        if self.is_current:
            border_style = "3px solid #3daee9"  # Синий (стандартный для выделения)

        style = f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: {border_style};
                border-radius: 8px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                border: 2px solid #aaaaaa;
            }}
        """
        self.setStyleSheet(style)


# ==========================================
# 5. Главное окно
# ==========================================

class TestRunnerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Testing System")
        self.resize(1000, 700)

        self.session: Optional[TestSession] = None
        self.exercises: List[ExerciseModel] = []
        self.nav_buttons: List[NavButton] = []
        self.current_index = -1

        # Таймер
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer_display)
        self.elapsed_seconds = 0
        self.current_exercise_start_time = 0

        self.init_ui()
        QTimer.singleShot(100, self.load_test_file)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной горизонтальный слой: [Навигация] | [Тест]
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # --- Левая панель (Навигация) ---
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_panel.setFixedWidth(75)  # Фиксированная ширина панели

        # Кнопка НАЗАД (Сверху)
        self.btn_prev = QPushButton("↑")
        self.btn_prev.clicked.connect(self.prev_exercise)
        self.btn_prev.setFixedHeight(40)
        left_layout.addWidget(self.btn_prev)

        # Скролл-зона для кнопок навигации
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        self.nav_container = QWidget()
        self.nav_grid = QGridLayout(self.nav_container)
        self.nav_grid.setAlignment(Qt.AlignTop)
        self.nav_grid.setSpacing(10)
        scroll.setWidget(self.nav_container)

        left_layout.addWidget(scroll)

        # Кнопка ВПЕРЕД (Снизу)
        self.btn_next = QPushButton("↓")
        self.btn_next.clicked.connect(self.next_exercise)
        self.btn_next.setFixedHeight(40)
        left_layout.addWidget(self.btn_next)

        main_layout.addWidget(left_panel)

        # --- Правая панель (Контент) ---
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Верхний бар: Spacer | Finish | Timer
        top_bar = QHBoxLayout()

        self.btn_finish = QPushButton("Завершить тест")
        self.btn_finish.clicked.connect(self.finish_test)
        # Обычный стиль для кнопки завершения

        self.timer_label = QLabel("00:00")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setFixedWidth(80)  # Чтобы не прыгал текст

        top_bar.addStretch()  # Растяжка слева
        top_bar.addWidget(self.btn_finish)
        top_bar.addWidget(self.timer_label)

        right_layout.addLayout(top_bar)

        # Стек с карточками
        self.stacked_widget = QStackedWidget()
        right_layout.addWidget(self.stacked_widget)

        main_layout.addWidget(right_panel)

        self.update_nav_buttons_state()

    def build_nav_grid(self):
        # Очистка старой сетки
        while self.nav_grid.count():
            item = self.nav_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.nav_buttons.clear()

        # Создание кнопок 3 в ряд
        cols = 1
        for i in range(len(self.exercises)):
            btn = NavButton(i)
            btn.clicked.connect(lambda checked, idx=i: self.switch_to_exercise(idx))
            self.nav_buttons.append(btn)
            self.nav_grid.addWidget(btn, i // cols, i % cols)

    def load_test_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Открыть файл теста", "", "JSON Files (*.json)")
        if not file_name:
            if not self.exercises:
                sys.exit()
            return

        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.exercises = [ExerciseModel(ex) for ex in data]
            self.start_test()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить тест:\n{e}")

    def start_test(self):
        self.session = TestSession()
        self.elapsed_seconds = 0

        # Пересоздаем стек
        while self.stacked_widget.count():
            widget = self.stacked_widget.widget(0)
            self.stacked_widget.removeWidget(widget)
            widget.deleteLater()

        for ex in self.exercises:
            widget = WidgetFactory.create_widget(ex)
            # При изменении ответа обновляем данные сессии и стиль кнопки
            widget.answerChanged.connect(lambda ans, eid=ex.id: self.on_answer_changed(eid, ans))
            self.stacked_widget.addWidget(widget)

        self.build_nav_grid()

        self.current_index = 0
        self.timer.start(1000)
        self.session.log_event("test_started")

        self.switch_to_exercise(0)

    def on_answer_changed(self, exercise_id, answer):
        self.session.record_answer(exercise_id, answer)
        # Обновляем стиль кнопок (чтобы появился флаг "решено")
        self.refresh_nav_styles()

    def refresh_nav_styles(self):
        for i, btn in enumerate(self.nav_buttons):
            ex_id = self.exercises[i].id
            has_ans = self.session.has_answer(ex_id)
            is_cur = (i == self.current_index)
            btn.set_state(is_cur, has_ans)

    def switch_to_exercise(self, index):
        if index < 0 or index >= len(self.exercises):
            return

        if self.current_index != -1 and self.current_index != index:
            prev_id = self.exercises[self.current_index].id
            duration = time.time() - self.current_exercise_start_time
            self.session.log_event("close_exercise", prev_id, {"duration_seconds": duration})

        self.current_index = index
        self.stacked_widget.setCurrentIndex(index)

        current_id = self.exercises[index].id
        self.current_exercise_start_time = time.time()
        self.session.log_event("open_exercise", current_id)

        self.update_nav_buttons_state()
        self.refresh_nav_styles()

    def update_nav_buttons_state(self):
        self.btn_prev.setEnabled(self.current_index > 0)
        self.btn_next.setEnabled(self.current_index < len(self.exercises) - 1)
        self.btn_finish.setEnabled(len(self.exercises) > 0)

    def next_exercise(self):
        self.switch_to_exercise(self.current_index + 1)

    def prev_exercise(self):
        self.switch_to_exercise(self.current_index - 1)

    def update_timer_display(self):
        self.elapsed_seconds += 1
        m, s = divmod(self.elapsed_seconds, 60)
        self.timer_label.setText(f"{m:02d}:{s:02d}")

    def finish_test(self):
        reply = QMessageBox.question(self, 'Завершение',
                                     "Завершить тест?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.timer.stop()
            last_id = self.exercises[self.current_index].id
            duration = time.time() - self.current_exercise_start_time
            self.session.log_event("close_exercise", last_id, {"duration_seconds": duration})

            self.session.log_event("test_finished")
            self.save_log()

    def save_log(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить результат",
                                                   f"log_{int(time.time())}.json",
                                                   "JSON Files (*.json)")
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(self.session.export_json())
                QMessageBox.information(self, "Успех", "Лог сохранен.")
                self.close()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении:\n{e}")

    def changeEvent(self, event):
        """Перехват изменения состояния окна (Active/Inactive)."""
        if event.type() == QEvent.ActivationChange:
            if self.isActiveWindow():
                if self.session: self.session.log_event("app_focus_gained")
            else:
                if self.session: self.session.log_event("app_focus_lost")
        super().changeEvent(event)


# ==========================================
# 6. Запуск и Генератор тестовых данных
# ==========================================
def create_dummy_test_file():
    test_data = [
        {
            "id": 1,
            "type": "single_choice",
            "question": "<h3>Вопрос 1</h3><p>Сколько будет 2 + 2?</p>",
            "options": ["3", "4", "5", "6"]
        },
        {
            "id": 2,
            "type": "multi_choice",
            "question": "<h3>Вопрос 2</h3><p>Выберите языки программирования:</p>",
            "options": ["Python", "HTML", "C++", "MP3"]
        },
        {
            "id": 3,
            "type": "ordering",
            "question": "<h3>Вопрос 3</h3><p>Порядок цветов радуги:</p>",
            "options": ["Охотник", "Каждый", "Желает", "Знать"]
        },
        {
            "id": 4,
            "type": "code",
            "question": "<h3>Вопрос 4</h3><p>Напишите функцию sum(a, b):</p>",
            "initial_code": "def sum(a, b):\n    pass"
        },
        {
            "id": 5,
            "type": "input",
            "question": "<h3>Вопрос 5</h3><p>Столица Франции?</p>"
        },
        {
            "id": 404,
            "type": "code_fragment",
            "question": "<h3>Исправьте ошибку</h3><p>Вставьте правильный оператор сравнения вместо прочерков, чтобы условие было истинным при x=10.</p>",
            "prefix": "x = 10\nif x ",
            "initial_code": "______",
            "suffix": " 5:\n    print('Больше')"
        },
    ]
    # Добавим больше вопросов для проверки скролла
    for i in range(6, 21):
        test_data.append({
            "id": i,
            "type": "input",
            "question": f"<h3>Вопрос {i}</h3><p>Введите любое значение:</p>"
        })

    with open("example_test.json", "w", encoding="utf-8") as f:
        json.dump(test_data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    import os

    # if not os.path.exists("example_test.json"):
    #     create_dummy_test_file()

    app = QApplication(sys.argv)

    # Глобальное увеличение шрифта
    font = app.font()
    font.setPointSize(int(font.pointSize() * 1.5))
    app.setFont(font)

    window = TestRunnerWindow()
    window.show()
    sys.exit(app.exec())