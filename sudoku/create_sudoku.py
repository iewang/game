import random


def is_valid(board, row, col, num):
    """检查数独中某个位置是否可以放入某个数字。"""
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for d in range(start_col, start_col + 3):
            if board[r][d] == num:
                return False
    return True


def solve_sudoku(board):
    """解决数独谜题。"""
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if solve_sudoku(board):
                            return True
                        board[i][j] = 0
                return False
    return True


def create_full_sudoku():
    """生成一个完整的数独棋盘。"""
    board = [[0] * 9 for _ in range(9)]

    # 随机填充对角的3x3方格
    def fill_diagonal_boxes():
        for i in range(0, 9, 3):
            fill_box(board, i, i)

    def fill_box(board, row, col):
        """在3x3方格中填入1到9的随机数字。"""
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                board[row + i][col + j] = nums.pop()

    def fill_remaining(i, j):
        """递归填充剩余的数独单元格。"""
        if j >= 9 and i < 8:
            i += 1
            j = 0
        if i >= 9 and j >= 9:
            return True
        if i < 3:
            if j < 3:
                j = 3
        elif i < 9 - 3:
            if j == int(i / 3) * 3:
                j += 3
        else:
            if j == 9 - 3:
                i += 1
                j = 0
                if i >= 9:
                    return True
        for num in range(1, 10):
            if is_valid(board, i, j, num):
                board[i][j] = num
                if fill_remaining(i, j + 1):
                    return True
                board[i][j] = 0
        return False

    fill_diagonal_boxes()
    fill_remaining(0, 3)
    return board


def has_unique_solution(board):
    """检查数独是否有且只有一个解。"""
    board_copy = [row[:] for row in board]  # 深复制
    return solve_and_count(board_copy) == 1


def solve_and_count(board, count=0):
    """计算数独的解的数量。"""
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        count = solve_and_count(board, count)
                        if count > 1:
                            return count
                        board[i][j] = 0
                return count
    return count + 1


def remove_numbers(board, num_remove):
    """从数独谜题中移除一定数量的数字以创建谜题，同时保持唯一解。"""
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    removed = 0

    for r, c in cells:
        if removed >= num_remove:
            break
        backup = board[r][c]
        board[r][c] = 0

        # 检查是否仍然是唯一解
        if has_unique_solution(board):
            removed += 1
        else:
            board[r][c] = backup  # 恢复原来的数字
    return board


def generate_sudoku(difficulty='medium'):
    """生成一个具有指定难度的数独谜题。"""
    if difficulty == 'easy':
        num_remove = 30
    elif difficulty == 'medium':
        num_remove = 40
    elif difficulty == 'hard':
        num_remove = 50
    else:
        num_remove = 40

    board = create_full_sudoku()
    board = remove_numbers(board, num_remove)
    return board


# 测试生成的数独
if __name__ == "__main__":
    sudoku = generate_sudoku('medium')
    for row in sudoku:
        print(row)
