from flask import Flask, render_template, jsonify, request, session
from minesweeper import Minesweeper
import os

app = Flask(__name__)
app.secret_key = 'minesweeper_secret_key_2024'

# 儲存遊戲實例
games = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/new_game', methods=['POST'])
def new_game():
    """建立新遊戲"""
    data = request.json
    rows = data.get('rows', 9)
    cols = data.get('cols', 9)
    mines = data.get('mines', 10)
    
    # 驗證參數
    if rows < 4 or cols < 4 or mines >= rows * cols:
        return jsonify({'error': '無效的遊戲參數'}), 400
    
    game_id = str(len(games))
    games[game_id] = Minesweeper(rows, cols, mines)
    
    return jsonify({
        'game_id': game_id,
        'rows': rows,
        'cols': cols,
        'mines': mines,
        'board': [['hidden' for _ in range(cols)] for _ in range(rows)]
    })

@app.route('/api/reveal', methods=['POST'])
def reveal():
    """翻開格子"""
    data = request.json
    game_id = data.get('game_id')
    r = data.get('row')
    c = data.get('col')
    
    if game_id not in games:
        return jsonify({'error': '遊戲不存在'}), 400
    
    game = games[game_id]
    game.reveal(r, c)
    
    return get_game_state(game_id)

@app.route('/api/flag', methods=['POST'])
def flag():
    """標記/取消旗幟"""
    data = request.json
    game_id = data.get('game_id')
    r = data.get('row')
    c = data.get('col')
    
    if game_id not in games:
        return jsonify({'error': '遊戲不存在'}), 400
    
    game = games[game_id]
    game.toggle_flag(r, c)
    
    return get_game_state(game_id)

@app.route('/api/state/<game_id>', methods=['GET'])
def state(game_id):
    """獲取遊戲狀態"""
    return get_game_state(game_id)

def get_game_state(game_id):
    """返回遊戲狀態JSON"""
    if game_id not in games:
        return jsonify({'error': '遊戲不存在'}), 400
    
    game = games[game_id]
    
    # 構建棋盤顯示
    board_display = []
    for r in range(game.rows):
        row = []
        for c in range(game.cols):
            cell_display = game.get_cell_display(r, c)
            row.append(cell_display)
        board_display.append(row)
    
    # 計算統計資訊
    flagged_count = sum(sum(row) for row in game.flags)
    remaining_mines = game.mines - flagged_count
    
    # 判斷遊戲狀態
    game_status = 'playing'
    if game.game_over:
        # 檢查是否贏
        if game._check_win():
            game_status = 'won'
        else:
            game_status = 'lost'
    
    return jsonify({
        'game_id': game_id,
        'board': board_display,
        'rows': game.rows,
        'cols': game.cols,
        'mines': game.mines,
        'remaining_mines': remaining_mines,
        'game_over': game.game_over,
        'status': game_status
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
