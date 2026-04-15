import random
import sys


class Minesweeper:
    def __init__(self, rows=9, cols=9, mines=10):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0] * cols for _ in range(rows)]
        self.visible = [[False] * cols for _ in range(rows)]
        self.flags = [[False] * cols for _ in range(rows)]
        self.game_over = False
        self.first_move = True
        self.mines_placed = False  # 標記地雷是否已放置

    def _place_mines_randomly(self, exclude_r=None, exclude_c=None):
        """放置地雷，排除指定的位置（用於第一步）"""
        positions = []
        for r in range(self.rows):
            for c in range(self.cols):
                if exclude_r is not None and exclude_c is not None:
                    if abs(r - exclude_r) <= 1 and abs(c - exclude_c) <= 1:
                        continue  # 排除點擊位置及其周圍8個格子
                positions.append((r, c))

        # 如果可放置位置不夠，重新選擇（不排除）
        if len(positions) < self.mines:
            positions = [(r, c) for r in range(self.rows) for c in range(self.cols)
                        if not (r == exclude_r and c == exclude_c)]

        random.shuffle(positions)
        for r, c in positions[:self.mines]:
            self.board[r][c] = -1
        self._calculate_numbers()

    def _calculate_numbers(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    continue
                count = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.board[nr][nc] == -1:
                                count += 1
                self.board[r][c] = count

    def _flood_fill(self, r, c):
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return
        if self.visible[r][c] or self.flags[r][c]:
            return
        self.visible[r][c] = True
        if self.board[r][c] != 0:
            return
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                self._flood_fill(r + dr, c + dc)

    def reveal(self, r, c):
        if self.game_over:
            return
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            print("座標不合法。請輸入正確的列和行。")
            return
        if self.flags[r][c]:
            print("這個位置已標記為旗幟，先取消旗幟再翻開。")
            return

        # 第一步特殊處理：先放置地雷，確保不會踩到地雷
        if self.first_move:
            self._place_mines_randomly(exclude_r=r, exclude_c=c)
            self.first_move = False
            self.mines_placed = True

        if self.board[r][c] == -1:
            self.game_over = True
            self._reveal_all()
            print("你輸了")
            return
        self._flood_fill(r, c)
        if self._check_win():
            self.game_over = True
            self._reveal_all()
            print("恭喜你，已經成功排除所有地雷！")

    def toggle_flag(self, r, c):
        if self.game_over:
            return
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            print("座標不合法。請輸入正確的列和行。")
            return
        if self.visible[r][c]:
            print("這個位置已經打開，無法標記旗幟。")
            return
        self.flags[r][c] = not self.flags[r][c]

    def _reveal_all(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.visible[r][c] = True

    def _check_win(self):
        if not self.mines_placed:
            return False  # 地雷還沒放置，不能判斷勝利
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != -1 and not self.visible[r][c]:
                    return False
        return True

    def print_board(self):
        header = '   ' + ' '.join(f'{c:2d}' for c in range(self.cols))
        print(header)
        for r in range(self.rows):
            row_str = f'{r:2d} '
            for c in range(self.cols):
                if self.flags[r][c]:
                    cell = 'F '
                elif not self.visible[r][c]:
                    cell = '· '
                else:
                    if self.board[r][c] == -1:
                        cell = '* '
                    elif self.board[r][c] == 0:
                        cell = '  '
                    else:
                        cell = f'{self.board[r][c]} '
                row_str += cell
            print(row_str)


    def get_state(self):
        """返回遊戲狀態用於API"""
        return {
            'board': self.board,
            'visible': self.visible,
            'flags': self.flags,
            'game_over': self.game_over,
            'rows': self.rows,
            'cols': self.cols,
            'mines': self.mines
        }

    def get_cell_display(self, r, c):
        """返回單個格子的顯示值"""
        if self.flags[r][c]:
            return 'flag'
        elif not self.visible[r][c]:
            return 'hidden'
        elif self.board[r][c] == -1:
            return 'mine'
        elif self.board[r][c] == 0:
            return 'empty'
        else:
            return str(self.board[r][c])


def main():
    print("歡迎來到踩地雷遊戲！")
    try:
        rows = int(input("請輸入行數（預設 9）：") or 9)
        cols = int(input("請輸入列數（預設 9）：") or 9)
        mines = int(input("請輸入地雷數（預設 10）：") or 10)
    except ValueError:
        print("請輸入有效的整數。")
        return

    game = Minesweeper(rows, cols, mines)

    while not game.game_over:
        game.print_board()
        command = input("操作：r row col（翻開） / f row col（標記） / q（退出） : ").strip().lower().split()
        if not command:
            continue
        action = command[0]
        if action == 'q':
            print("已退出遊戲。")
            break
        if len(command) != 3:
            print("請輸入正確指令格式，例如：r 3 4 或 f 2 1")
            continue
        try:
            r = int(command[1])
            c = int(command[2])
        except ValueError:
            print("行列必須是整數。")
            continue
        if action == 'r':
            game.reveal(r, c)
        elif action == 'f':
            game.toggle_flag(r, c)
        else:
            print("未知指令，請使用 r、f 或 q。")

    game.print_board()


if __name__ == '__main__':
    main()
