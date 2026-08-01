"""ScrnshotMate 的設計 token 與全域樣式。

色階以 icon 的青綠 (#43889b, OKLCH hue 218) 為基準推導，
文字對背景一律 >= 4.5:1。
"""

from PySide6.QtCore import Qt

LIGHT = {
    "bg": "#eff4f6",
    "surface": "#fbfeff",
    "sunken": "#e2e9eb",
    "border": "#d1d9dc",
    "ink": "#1b292d",
    "ink_muted": "#637175",
    "accent": "#23798f",
    "accent_hover": "#0d6c81",
    "accent_active": "#006175",
    "accent_subtle": "#cfeef8",
    "focus": "#269ab5",
    "danger": "#b2403d",
    "danger_subtle": "#ffe3df",
    "success": "#347c48",
    "disabled_bg": "#dbe1e2",
    "disabled_ink": "#9a9fa1",
    "on_accent": "#ffffff",
    "canvas": "#14191b",
}

DARK = {
    "bg": "#12181a",
    "surface": "#1e2426",
    "sunken": "#0a0f11",
    "border": "#343c3f",
    "ink": "#e9eeef",
    "ink_muted": "#879497",
    "accent": "#187990",
    "accent_hover": "#2f8aa1",
    "accent_active": "#006e84",
    "accent_subtle": "#103b46",
    "focus": "#3fa6c0",
    "danger": "#ea7972",
    "danger_subtle": "#4e2320",
    "success": "#58a069",
    "disabled_bg": "#2d3334",
    "disabled_ink": "#6b7173",
    "on_accent": "#ffffff",
    "canvas": "#14191b",
}

# 4 的倍數，供 layout margin/spacing 使用（QSS 管不到 layout）
SPACE = {"xs": 4, "sm": 8, "md": 12, "lg": 16, "xl": 24, "2xl": 32, "3xl": 48}

FONT_SIZE = {"xs": 11, "sm": 12, "base": 13, "md": 15, "lg": 19, "xl": 28}

RADIUS = {"sm": 4, "md": 6, "lg": 10}

_QSS = """
* { font-size: %(fs_base)dpx; }

QMainWindow, QDialog { background-color: %(bg)s; }
QWidget { background-color: transparent; color: %(ink)s; }
QMainWindow > QWidget, QDialog > QWidget { background-color: %(bg)s; }

QToolTip {
    background-color: %(ink)s; color: %(surface)s;
    border: none; border-radius: %(r_sm)dpx; padding: 4px 8px;
}

/* ---- surfaces ---- */
QWidget#contentSurface { background-color: %(surface)s; border-radius: %(r_lg)dpx; }
QWidget#chromeBar { background-color: %(bg)s; }

/* ---- buttons ---- */
QPushButton {
    background-color: %(surface)s;
    color: %(ink)s;
    border: 1px solid %(border)s;
    border-radius: %(r_sm)dpx;
    padding: 6px 14px;
    min-height: 18px;
}
QPushButton:hover { background-color: %(sunken)s; border-color: %(ink_muted)s; }
QPushButton:pressed { background-color: %(border)s; }
QPushButton:focus { border-color: %(focus)s; outline: none; }
QPushButton:disabled {
    background-color: %(disabled_bg)s; color: %(disabled_ink)s; border-color: %(disabled_bg)s;
}

QPushButton[variant="primary"] {
    background-color: %(accent)s; color: %(on_accent)s;
    border: 1px solid %(accent)s; font-weight: 600;
}
QPushButton[variant="primary"]:hover {
    background-color: %(accent_hover)s; border-color: %(accent_hover)s;
}
QPushButton[variant="primary"]:pressed {
    background-color: %(accent_active)s; border-color: %(accent_active)s;
}
QPushButton[variant="primary"]:focus { border-color: %(focus)s; }
QPushButton[variant="primary"]:disabled {
    background-color: %(disabled_bg)s; color: %(disabled_ink)s; border-color: %(disabled_bg)s;
}

QPushButton[variant="ghost"] {
    background-color: transparent; border-color: transparent; color: %(ink_muted)s;
}
QPushButton[variant="ghost"]:hover { background-color: %(sunken)s; color: %(ink)s; }

/* ---- text inputs ---- */
QLineEdit, QSpinBox, QComboBox {
    background-color: %(surface)s;
    color: %(ink)s;
    border: 1px solid %(border)s;
    border-radius: %(r_sm)dpx;
    padding: 5px 8px;
    selection-background-color: %(accent)s;
    selection-color: %(on_accent)s;
}
QLineEdit:hover, QSpinBox:hover, QComboBox:hover { border-color: %(ink_muted)s; }
QLineEdit:focus, QSpinBox:focus, QComboBox:focus { border-color: %(focus)s; }
QLineEdit:disabled, QSpinBox:disabled, QComboBox:disabled {
    background-color: %(disabled_bg)s; color: %(disabled_ink)s;
}
QLineEdit[placeholderText] { color: %(ink)s; }

QComboBox QAbstractItemView {
    background-color: %(surface)s; color: %(ink)s;
    border: 1px solid %(border)s; border-radius: %(r_sm)dpx;
    selection-background-color: %(accent)s; selection-color: %(on_accent)s;
    outline: none;
}

/* ---- group box ---- */
QGroupBox {
    background-color: %(surface)s;
    border: 1px solid %(border)s;
    border-radius: %(r_md)dpx;
    margin-top: 10px;
    padding: %(sp_lg)dpx %(sp_md)dpx %(sp_md)dpx %(sp_md)dpx;
    font-weight: 600;
}
QGroupBox::title {
    subcontrol-origin: margin; subcontrol-position: top left;
    left: %(sp_md)dpx; padding: 0 4px;
    color: %(ink)s;
}

/* ---- radio / check ---- */
/* 一旦對 QRadioButton 設樣式，Qt 就停用原生 indicator 繪製，必須自己補齊 */
QRadioButton, QCheckBox { color: %(ink)s; spacing: 8px; padding: 3px 0; }
QRadioButton:disabled, QCheckBox:disabled { color: %(disabled_ink)s; }

QRadioButton::indicator, QCheckBox::indicator {
    width: 15px; height: 15px;
    background: %(surface)s;
    border: 1px solid %(ink_muted)s;
}
QRadioButton::indicator { border-radius: 8px; }
QCheckBox::indicator { border-radius: %(r_sm)dpx; }
QRadioButton::indicator:hover, QCheckBox::indicator:hover { border-color: %(accent)s; }
/* 實心圓而非甜甜圈：Qt 對粗 border 搭 border-radius 會畫成方角 */
QRadioButton::indicator:checked {
    background: %(accent)s;
    border: 1px solid %(accent)s;
    border-radius: 8px;
}
QCheckBox::indicator:checked {
    background: %(accent)s;
    border-color: %(accent)s;
}
QRadioButton::indicator:disabled, QCheckBox::indicator:disabled {
    background: %(disabled_bg)s; border-color: %(disabled_ink)s;
}

/* ---- slider ---- */
QSlider::groove:horizontal {
    height: 4px; background: %(border)s; border-radius: 2px;
}
QSlider::sub-page:horizontal { background: %(accent)s; border-radius: 2px; }
QSlider::handle:horizontal {
    width: 14px; height: 14px; margin: -5px 0;
    background: %(surface)s; border: 1px solid %(ink_muted)s; border-radius: 7px;
}
QSlider::handle:horizontal:hover { border-color: %(accent)s; }

/* ---- list ---- */
QListWidget {
    background-color: %(surface)s;
    border: 1px solid %(border)s;
    border-radius: %(r_md)dpx;
    outline: none;
    padding: %(sp_sm)dpx;
}
QListWidget::item {
    color: %(ink)s;
    border: 1px solid transparent;
    border-radius: %(r_sm)dpx;
    padding: %(sp_sm)dpx;
}
QListWidget::item:hover { background-color: %(sunken)s; }
QListWidget::item:selected {
    background-color: %(accent_subtle)s;
    border-color: %(accent)s;
    color: %(ink)s;
}

/* ---- scrollbar ---- */
QScrollBar:vertical { background: transparent; width: 10px; margin: 0; }
QScrollBar::handle:vertical {
    background: %(border)s; border-radius: 5px; min-height: 30px;
}
QScrollBar::handle:vertical:hover { background: %(ink_muted)s; }
QScrollBar:horizontal { background: transparent; height: 10px; margin: 0; }
QScrollBar::handle:horizontal {
    background: %(border)s; border-radius: 5px; min-width: 30px;
}
QScrollBar::handle:horizontal:hover { background: %(ink_muted)s; }
QScrollBar::add-line, QScrollBar::sub-line { height: 0; width: 0; }
QScrollBar::add-page, QScrollBar::sub-page { background: transparent; }

/* ---- progress ---- */
QProgressBar {
    background-color: %(sunken)s; border: none;
    border-radius: %(r_sm)dpx; height: 6px; text-align: center;
}
QProgressBar::chunk { background-color: %(accent)s; border-radius: %(r_sm)dpx; }

/* ---- label roles ---- */
QLabel { background: transparent; color: %(ink)s; }
QLabel[role="muted"] { color: %(ink_muted)s; font-size: %(fs_sm)dpx; }
QLabel[role="fieldLabel"] { color: %(ink_muted)s; }
QLabel[role="title"] { font-size: %(fs_lg)dpx; font-weight: 600; }
QLabel[role="display"] { font-size: %(fs_xl)dpx; font-weight: 600; letter-spacing: -0.5px; }
QLabel[role="version"] { color: %(ink_muted)s; font-size: %(fs_xs)dpx; }
QLabel[role="hint"] { color: %(ink_muted)s; font-size: %(fs_md)dpx; }
QLabel[role="status"] { color: %(ink_muted)s; }
QLabel[role="statusOk"] { color: %(success)s; }
QLabel[role="statusWarn"] { color: %(danger)s; font-weight: 600; }
QLabel[role="preview"] { color: %(ink_muted)s; }

/* ---- drop zone ---- */
QFrame#dropZone {
    background-color: %(surface)s;
    border: 2px dashed %(border)s;
    border-radius: %(r_lg)dpx;
}
QFrame#dropZone[dragging="true"] {
    background-color: %(accent_subtle)s;
    border: 2px dashed %(accent)s;
}

/* ---- crop canvas ---- */
QGraphicsView#cropCanvas {
    background-color: %(canvas)s;
    border: 1px solid %(border)s;
    border-radius: %(r_md)dpx;
}
"""


def tokens_for(scheme):
    return DARK if scheme == Qt.ColorScheme.Dark else LIGHT


def repolish(widget):
    """改過 property 之後強制 Qt 重算樣式。"""
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    widget.update()


def build_qss(t):
    return _QSS % {
        "fs_xs": FONT_SIZE["xs"], "fs_sm": FONT_SIZE["sm"], "fs_base": FONT_SIZE["base"],
        "fs_md": FONT_SIZE["md"], "fs_lg": FONT_SIZE["lg"], "fs_xl": FONT_SIZE["xl"],
        "r_sm": RADIUS["sm"], "r_md": RADIUS["md"], "r_lg": RADIUS["lg"],
        "sp_sm": SPACE["sm"], "sp_md": SPACE["md"], "sp_lg": SPACE["lg"],
        **t,
    }


_current = dict(LIGHT)


def current():
    """目前生效的 token，供無法用 QSS 表達的繪圖程式碼取用。"""
    return _current


def apply_theme(app):
    """套用主題，並在系統亮暗切換時自動重刷。"""
    from PySide6.QtGui import QFontDatabase
    app.setFont(QFontDatabase.systemFont(QFontDatabase.SystemFont.GeneralFont))

    def refresh():
        global _current
        _current = tokens_for(app.styleHints().colorScheme())
        app.setStyleSheet(build_qss(_current))

    refresh()
    app.styleHints().colorSchemeChanged.connect(lambda _: refresh())
