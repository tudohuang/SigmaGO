def find_legal_moves(board, previous_board, player):
    def is_on_board(i, j):
        return 0 <= i < 9 and 0 <= j < 9

    def get_adjacent(i, j):
        return [(x, y) for x, y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)] if is_on_board(x, y)]

    def get_liberties(i, j):
        return sum(1 for x, y in get_adjacent(i, j) if board[x][y] == 0)

    def would_capture(i, j, player):
        return any(board[x][y] == -player and get_liberties(x, y) == 1 for x, y in get_adjacent(i, j))

    def apply_move(temp_board, i, j, player):
        temp_board[i][j] = player
        for x, y in get_adjacent(i, j):
            if temp_board[x][y] == -player and get_liberties(x, y) == 0:
                remove_captured_stones(temp_board, x, y, -player)

    def remove_captured_stones(temp_board, i, j, player):
        if is_on_board(i, j) and temp_board[i][j] == player:
            temp_board[i][j] = 0
            for x, y in get_adjacent(i, j):
                remove_captured_stones(temp_board, x, y, player)

    def is_ko(i, j, player):
        temp_board = [row[:] for row in board]
        apply_move(temp_board, i, j, player)
        return temp_board == previous_board

    legal_moves = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                if get_liberties(i, j) > 0 or would_capture(i, j, player):
                    if not is_ko(i, j, player):
                        legal_moves.append((i, j))

    return legal_moves

# Example usage
current_board = [[0 for _ in range(9)] for _ in range(9)]  # current empty 9x9 Go board
previous_board = [[0 for _ in range(9)] for _ in range(9)]  # previous board state
player = 1  # 1 for white, -1 for black
legal_moves = find_legal_moves(current_board, previous_board, player)
print(legal_moves)
