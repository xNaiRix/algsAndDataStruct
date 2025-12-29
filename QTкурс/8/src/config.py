from typing import Literal

# Настройки сцены
DEFAULT_SCENE_WIDTH = 800
DEFAULT_SCENE_HEIGHT = 600
BG_COLOR = "white"

# Настройки фигур
DEFAULT_STROKE_WIDTH = 2
DEFAULT_COLOR = "#000000"

# Типы фигур (чтобы не писать строки "rect" вручную и не опечатываться)
TYPE_RECT = "rect"
TYPE_LINE = "line"
TYPE_ELLIPSE = "ellipse"
TYPE_GROUP = "group"

TOOL_RECT = "rect"
TOOL_LINE = "line"
TOOL_ELLIPSE = "ellipse"
TOOL_SELECT = "select"

ToolName = Literal[TOOL_RECT, TOOL_LINE, TOOL_ELLIPSE, TOOL_SELECT]
FigureName = Literal[TYPE_RECT, TYPE_LINE, TYPE_ELLIPSE, TYPE_GROUP]
ShapeName = Literal[TYPE_RECT, TYPE_LINE, TYPE_ELLIPSE]

UNDO_LIMIT = 50