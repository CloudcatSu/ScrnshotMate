import os
from collections import Counter
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QSlider, QLabel, QPushButton, QFileDialog, QStackedWidget, QFrame
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon, QPixmap, QColor, QPainter, QPen
from core.image_processor import get_image_info
from ui import theme

class PreviewGrid(QWidget):
    # Signals to communicate with MainWindow
    files_changed = Signal(bool) # True if all valid and > 0, False otherwise

    def __init__(self):
        super().__init__()
        self.image_data = [] # List of dicts with file info
        self.majority_size = None
        self.has_anomalies = False

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(theme.SPACE["md"])

        self.stack = QStackedWidget()
        
        # Empty State Widget (Drop Zone)
        self.empty_widget = QWidget()
        empty_outer_layout = QVBoxLayout(self.empty_widget)
        empty_outer_layout.setContentsMargins(theme.SPACE["xl"], theme.SPACE["xl"], theme.SPACE["xl"], theme.SPACE["xl"])
        
        self.drop_zone = QFrame()
        self.drop_zone.setObjectName("dropZone")
        self.drop_zone.setProperty("dragging", False)
        theme.repolish(self.drop_zone)
        
        empty_layout = QVBoxLayout(self.drop_zone)
        empty_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Icon
        self.lbl_icon = QLabel()
        from utils.helpers import resource_path
        icon_path = resource_path(os.path.join("assets", "ScrnshotMate_icon.png"))
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            self.lbl_icon.setPixmap(pixmap.scaledToWidth(96, Qt.TransformationMode.SmoothTransformation))
        self.lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title
        lbl_title = QLabel("ScrnshotMate")
        lbl_title.setProperty("role", "display")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        theme.repolish(lbl_title)
        
        # Version
        from utils.helpers import APP_VERSION
        lbl_version = QLabel(f"v{APP_VERSION}")
        lbl_version.setProperty("role", "version")
        lbl_version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        theme.repolish(lbl_version)
        
        # Hint
        lbl_hint = QLabel("把圖片拖到這裡")
        lbl_hint.setProperty("role", "hint")
        lbl_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        theme.repolish(lbl_hint)
        
        # Muted
        lbl_muted = QLabel("支援 PNG、JPG、WebP、BMP、TIFF")
        lbl_muted.setProperty("role", "muted")
        lbl_muted.setAlignment(Qt.AlignmentFlag.AlignCenter)
        theme.repolish(lbl_muted)
        
        # Button
        btn_browse = QPushButton("選擇檔案")
        btn_browse.setProperty("variant", "primary")
        theme.repolish(btn_browse)
        btn_browse.clicked.connect(self.browse_files)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn_browse)
        btn_layout.addStretch()
        
        empty_layout.addStretch()
        empty_layout.addWidget(self.lbl_icon)
        empty_layout.addWidget(lbl_title)
        empty_layout.addWidget(lbl_version)
        empty_layout.addSpacing(theme.SPACE["xl"])
        empty_layout.addWidget(lbl_hint)
        empty_layout.addWidget(lbl_muted)
        empty_layout.addSpacing(theme.SPACE["lg"])
        empty_layout.addLayout(btn_layout)
        empty_layout.addStretch()
        
        empty_outer_layout.addWidget(self.drop_zone)

        # The Grid
        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        self.list_widget.setIconSize(QSize(150, 150))
        self.list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.list_widget.setSpacing(theme.SPACE["md"])
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.list_widget.setWordWrap(True)
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)
        
        self.stack.addWidget(self.empty_widget)
        self.stack.addWidget(self.list_widget)

        layout.addWidget(self.stack)
        
        # Status Label
        self.status_label = QLabel("尚未載入圖片")
        self.status_label.setProperty("role", "status")
        self.status_label.setWordWrap(True)
        theme.repolish(self.status_label)
        layout.addWidget(self.status_label)
        
        # Enable dragging to rearrange or drop files
        self.setAcceptDrops(True)

        # Bottom control bar
        control_layout = QHBoxLayout()
        control_layout.setSpacing(theme.SPACE["sm"])
        self.control_layout = control_layout
        
        self.add_btn = QPushButton("增加檔案")
        self.add_btn.clicked.connect(self.browse_files)
        
        self.delete_btn = QPushButton("刪除選取")
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.delete_selected)
        
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(50, 300)
        self.slider.setValue(150)
        self.slider.setFixedWidth(150)
        self.slider.valueChanged.connect(self.change_icon_size)
        
        lbl_slider = QLabel("縮圖大小")
        lbl_slider.setProperty("role", "fieldLabel")
        theme.repolish(lbl_slider)

        control_layout.addWidget(self.add_btn)
        control_layout.addWidget(self.delete_btn)
        control_layout.addStretch()
        control_layout.addWidget(lbl_slider)
        control_layout.addWidget(self.slider)

        layout.addLayout(control_layout)

    def _set_dragging(self, dragging):
        self.drop_zone.setProperty("dragging", dragging)
        theme.repolish(self.drop_zone)

    def add_primary_action(self, button):
        """讓主要動作按鈕併入底部控制列，不另起一行。"""
        self.control_layout.addSpacing(theme.SPACE["lg"])
        self.control_layout.addWidget(button)

    @staticmethod
    def _outline(pixmap, color):
        # 異常標示畫進縮圖，因為 QSS 的 ::item:selected 會蓋掉 setBackground
        w = max(4, pixmap.width() // 40)
        marked = QPixmap(pixmap)
        painter = QPainter(marked)
        painter.setPen(QPen(QColor(color), w))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(w // 2, w // 2, marked.width() - w, marked.height() - w)
        painter.end()
        return marked

    def change_icon_size(self, size):
        self.list_widget.setIconSize(QSize(size, size))

    def browse_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "選擇圖片", "", "Images (*.png *.jpg *.jpeg *.webp *.bmp *.tiff)"
        )
        if files:
            self.add_files(files)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self._set_dragging(True)
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self._set_dragging(False)

    def dropEvent(self, event):
        self._set_dragging(False)
        urls = event.mimeData().urls()
        files = [u.toLocalFile() for u in urls if u.isLocalFile()]
        if files:
            self.add_files(files)
            event.acceptProposedAction()

    def add_files(self, files):
        valid_exts = {'.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff'}
        new_files = [f for f in files if os.path.splitext(f)[1].lower() in valid_exts]
        
        for f in new_files:
            if not any(d['path'] == f for d in self.image_data):
                info = get_image_info(f)
                if info:
                    self.image_data.append(info)
        
        self.update_grid()

    def on_selection_changed(self):
        self.delete_btn.setEnabled(len(self.list_widget.selectedItems()) > 0)

    def delete_selected(self):
        items = self.list_widget.selectedItems()
        if not items:
            return
            
        for item in items:
            path = item.data(Qt.ItemDataRole.UserRole)
            self.image_data = [d for d in self.image_data if d['path'] != path]
            
        self.update_grid()

    def update_grid(self):
        self.list_widget.clear()
        
        if not self.image_data:
            self.stack.setCurrentIndex(0)
            self.status_label.setText("尚未載入圖片")
            self.status_label.setProperty("role", "status")
            theme.repolish(self.status_label)
            self.files_changed.emit(False)
            return

        self.stack.setCurrentIndex(1)

        # Calculate majority size
        sizes = [(d['width'], d['height']) for d in self.image_data]
        counter = Counter(sizes)
        self.majority_size = counter.most_common(1)[0][0]

        self.has_anomalies = False

        for data in self.image_data:
            path = data['path']
            filename = os.path.basename(path)
            w, h = data['width'], data['height']
            
            is_anomaly = (w, h) != self.majority_size
            if is_anomaly:
                self.has_anomalies = True

            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, path)
            
            label_text = f"{filename}\n{w}x{h}"
            item.setText(label_text)
            
            if is_anomaly:
                item.setText(f"⚠ {label_text}")

            pixmap = QPixmap(path)
            if not pixmap.isNull():
                if is_anomaly:
                    pixmap = self._outline(pixmap, theme.current()["danger"])
                item.setIcon(QIcon(pixmap))

            self.list_widget.addItem(item)

            if is_anomaly:
                item.setForeground(QColor(theme.current()["danger"]))
                item.setSelected(True)  # 須在 addItem 之後才會生效
            else:
                item.setForeground(QColor(theme.current()["ink"]))

        # Update status
        if self.has_anomalies:
            self.status_label.setText(f"有圖片尺寸與其他不同（多數為 {self.majority_size[0]}x{self.majority_size[1]}），請刪除已選取的異常圖片")
            self.status_label.setProperty("role", "statusWarn")
            theme.repolish(self.status_label)
            self.files_changed.emit(False)
        else:
            self.status_label.setText(f"{len(self.image_data)} 張圖片，尺寸皆為 {self.majority_size[0]}x{self.majority_size[1]}")
            self.status_label.setProperty("role", "statusOk")
            theme.repolish(self.status_label)
            self.files_changed.emit(True)

    def get_valid_files(self):
        if self.has_anomalies:
            return []
        return [d['path'] for d in self.image_data]
