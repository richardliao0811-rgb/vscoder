let currentGame = null;
let gameTimer = null;
let timeElapsed = 0;

async function startGame(rows, cols, mines) {
    try {
        const response = await fetch('/api/new_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ rows, cols, mines })
        });

        const data = await response.json();
        currentGame = data;
        timeElapsed = 0;
        startTimer();
        renderBoard();
        document.getElementById('gameContainer').style.display = 'block';
        updateStatus();
    } catch (error) {
        console.error('Error starting game:', error);
        alert('無法開始遊戲');
    }
}

function startCustomGame() {
    const rows = parseInt(document.getElementById('customRows').value);
    const cols = parseInt(document.getElementById('customCols').value);
    const mines = parseInt(document.getElementById('customMines').value);

    if (rows < 4 || cols < 4 || mines < 1 || mines >= rows * cols) {
        alert('請輸入有效的遊戲參數！\n行數和列數至少為4\n地雷數必須小於總格子數');
        return;
    }

    startGame(rows, cols, mines);
}

function resetGame() {
    if (currentGame) {
        startGame(currentGame.rows, currentGame.cols, currentGame.mines);
    }
}

function startTimer() {
    if (gameTimer) clearInterval(gameTimer);
    gameTimer = setInterval(() => {
        timeElapsed++;
        updateTimer();
    }, 1000);
}

function stopTimer() {
    if (gameTimer) clearInterval(gameTimer);
}

function updateTimer() {
    const minutes = Math.floor(timeElapsed / 60);
    const seconds = timeElapsed % 60;
    document.getElementById('timer').textContent = 
        `${minutes}:${seconds.toString().padStart(2, '0')}`;
}

async function revealCell(row, col) {
    if (!currentGame || currentGame.game_over) return;

    try {
        const response = await fetch('/api/reveal', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                game_id: currentGame.game_id,
                row: row,
                col: col
            })
        });

        const data = await response.json();
        currentGame = data;
        renderBoard();
        updateStatus();

        if (data.game_over) {
            stopTimer();
        }
    } catch (error) {
        console.error('Error revealing cell:', error);
    }
}

async function toggleFlag(row, col) {
    if (!currentGame || currentGame.game_over) return;

    try {
        const response = await fetch('/api/flag', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                game_id: currentGame.game_id,
                row: row,
                col: col
            })
        });

        const data = await response.json();
        currentGame = data;
        renderBoard();
        updateStatus();
    } catch (error) {
        console.error('Error toggling flag:', error);
    }
}

function renderBoard() {
    const boardElement = document.getElementById('board');
    boardElement.innerHTML = '';
    
    if (!currentGame) return;

    const cols = currentGame.cols;
    boardElement.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;

    for (let r = 0; r < currentGame.rows; r++) {
        for (let c = 0; c < cols; c++) {
            const cellValue = currentGame.board[r][c];
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.id = `cell-${r}-${c}`;

            // 設置格子的樣式和內容
            if (cellValue === 'hidden') {
                cell.classList.add('hidden');
                cell.textContent = '';
            } else if (cellValue === 'flag') {
                cell.classList.add('flagged');
                cell.textContent = '🚩';
            } else if (cellValue === 'empty') {
                cell.classList.add('empty');
                cell.textContent = '';
            } else if (cellValue === 'mine') {
                cell.classList.add('mine');
                cell.classList.add('clicked');
                cell.textContent = '💣';
            } else if (!isNaN(cellValue)) {
                const numValue = parseInt(cellValue);
                cell.classList.add('clicked');
                cell.classList.add(`num-${numValue}`);
                cell.textContent = numValue || '';
            }

            // 添加事件監聽
            cell.addEventListener('click', (e) => {
                e.preventDefault();
                if (cellValue === 'hidden') {
                    revealCell(r, c);
                }
            });

            cell.addEventListener('contextmenu', (e) => {
                e.preventDefault();
                if (cellValue === 'hidden') {
                    toggleFlag(r, c);
                }
            });

            boardElement.appendChild(cell);
        }
    }
}

function updateStatus() {
    const statusElement = document.getElementById('gameStatus');
    const minesElement = document.getElementById('minesRemaining');

    minesElement.textContent = currentGame.remaining_mines;

    if (currentGame.status === 'playing') {
        statusElement.textContent = '遊戲進行中...';
        statusElement.className = 'game-status playing';
    } else if (currentGame.status === 'won') {
        statusElement.textContent = '🎉 恭喜！你贏了！🎉';
        statusElement.className = 'game-status won';
        stopTimer();
    } else if (currentGame.status === 'lost') {
        statusElement.textContent = '💥 踩到地雷了！遊戲結束';
        statusElement.className = 'game-status lost';
        stopTimer();
    }
}

// 初始化頁面
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('gameContainer').style.display = 'none';
    document.getElementById('minesRemaining').textContent = '-';
});
