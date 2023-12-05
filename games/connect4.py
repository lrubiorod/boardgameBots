from game import Game


class ConnectFour(Game):
    def __init__(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.current_winner = None

    def print_board(self):
        print(' 1 2 3 4 5 6 7')
        for row in self.board:
            print('|' + '|'.join(row) + '|')
        print()
        print(f'Current winner: {self.current_winner}')

    def make_move(self, move, player):
        column = move
        if self.board[0][column] != ' ':
            return False

        row = next(row for row in reversed(self.board) if row[column] == ' ')
        row[column] = 'X' if player == 1 else 'O'

        if self.check_winner(column, row, player):
            self.current_winner = player
        return True

    def undo_move(self, move):
        column = move
        for row in self.board:
            if row[column] != ' ':
                row[column] = ' '
                break

        self.current_winner = None

    def check_winner(self, column, row, player):
        letter = 'X' if player == 1 else 'O'
        # Check horizontal, vertical, and both diagonals
        row_index = self.board.index(row)
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 0
            for i in range(-3, 4):
                r, c = row_index + dr * i, column + dc * i
                if 0 <= r < 6 and 0 <= c < 7 and self.board[r][c] == letter:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
        return False

    def get_available_moves(self):
        return [i for i in [3, 2, 4, 1, 5, 0, 6] if self.board[0][i] == ' ']

    def is_game_over(self):
        return self.current_winner is not None or all(self.board[0][i] != ' ' for i in range(7))

    def evaluate_game_state(self, player):
        if self.current_winner:
            return 1 if self.current_winner == player else -1
        else:
            return 0
