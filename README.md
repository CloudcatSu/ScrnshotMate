# ScrnshotMate

一個針對線上課程或會議全畫面截圖的自動化批次裁切工具。
在第一張圖片上定義裁切區域，即可自動批次裁切其他相同尺寸與解析度的圖片。

**目前版本：v1.2.0**（2026/07/11）｜完整更新記錄見 [CHANGELOG.md](CHANGELOG.md)

## 功能特色

- 以第一張圖片為範例，互動式拖拉設定裁切框
- 批次裁切，支援數十張以上的圖片
- 自動偵測尺寸異常的圖片並醒目警示
- 兩種輸出模式：覆蓋原檔（原圖丟至垃圾桶可還原）或另存新檔
- 支援輸出 JPG / PNG / WEBP，或將所有圖片合併為單一 PDF
- 彈性的批次命名規則（取代文字、加前後綴、連續編號），附即時預覽
- 同名檔案自動加上 ` (1)`、` (2)`…，不覆蓋既有檔案
- 完全離線執行，不上傳任何資料

## 系統要求

- macOS 14.0 或更高版本
- Apple Silicon（M 系列晶片）Mac

## 安裝

1. 下載 `ScrnshotMate.dmg` 並開啟，將 App 拖入「應用程式」資料夾。
2. 本 App 未經 Apple 公證，首次開啟若出現「身份不明的開發者」警告，請至「系統設定 → 隱私與安全性」點選「仍然開啟」。

## 從原始碼執行

```bash
# 建立虛擬環境並安裝依賴
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 執行
python main.py
```

### 打包為 .app

```bash
pip install pyinstaller
pyinstaller ScrnshotMate.spec --clean
```

## 專案結構

```
ScrnshotMate/
├── main.py               # 程式進入點
├── core/                 # 圖片裁切與批次處理邏輯
├── ui/                   # PySide6 介面（預覽格線、裁切編輯器、匯出對話框）
├── utils/                # 工具函式與版號定義
├── assets/               # App 圖示等靜態資源
├── docs/                 # 需求規格文件
└── ScrnshotMate.spec     # PyInstaller 打包設定
```

## 技術棧

- **語言**：Python 3.12
- **UI 框架**：PySide6（Qt for Python）
- **圖片處理**：Pillow
- **打包**：PyInstaller + create-dmg

## 開發歷程

本專案為 Su Sheng-Feng（CloudcatSu）的第一個公開 Vibe-coding 作品：

- **2026/04 起**：由 Antigravity（AI Agent，使用 Claude 3.5 Sonnet / Gemma 4）協作開發
- **2026/07/11 起**：AI 協作角色由 **Claude Code** 接手

## 授權

[MIT License](LICENSE)
