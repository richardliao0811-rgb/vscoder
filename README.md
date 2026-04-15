# 🎮 踩地雷遊戲 - Web版本

這是一個使用 Python Flask 和 JavaScript 建立的網頁踩地雷遊戲。

## 功能特色

- ✨ 精美的現代UI設計
- 🎯 三個預設難度等級（簡單、中等、困難）
- 🎨 自訂遊戲參數
- ⏱️ 遊戲計時器
- 🚩 旗幟標記地雷
- 📱 響應式設計，支援行動設備
- 🎉 遊戲勝負判定

## 安裝

### 環境要求
- Python 3.7+

### 安裝依賴

```bash
pip install -r requirements.txt
```

如果使用 Python 3.14：
```bash
python3.14 -m pip install -r requirements.txt
```

## 運行遊戲

```bash
python app.py
```

或使用 Python 3.14：
```bash
C:/Users/lesso/.local/bin/python3.14.exe app.py
```

然後在瀏覽器中開啟：
```
http://localhost:5000
```

## 遊戲規則

- **左鍵點擊**：翻開格子
- **右鍵點擊**：標記/取消旗幟
- **同時點擊**：在已打開的數字上同時點擊，快速打開周圍格子（需要周圍旗幟數等於該數字）

## 難度選項

- **簡單**：9×9 棋盤，10個地雷
- **中等**：16×16 棋盤，40個地雷
- **困難**：16×30 棋盤，99個地雷

## 項目結構

```
├── app.py                  # Flask應用主文件
├── minesweeper.py         # 遊戲邏輯核心
├── requirements.txt       # Python依賴
├── templates/
│   └── index.html        # HTML模板
└── static/
    ├── style.css         # 樣式表
    └── game.js           # 客戶端邏輯
```

## 技術棧

- **後端**：Flask（Python Web框架）
- **前端**：HTML5、CSS3、JavaScript（ES6+）
- **遊戲引擎**：Python類基礎

## API 端點

- `GET /` - 返回主頁面
- `POST /api/new_game` - 建立新遊戲
- `POST /api/reveal` - 翻開格子
- `POST /api/flag` - 標記或取消旗幟
- `GET /api/state/<game_id>` - 獲取遊戲狀態

## 許可證

MIT License
