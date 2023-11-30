from game import Game


class TicTacToe(Game):
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        print('***************')
        for row in range(3):
            print('| ' + ' | '.join(self.board[row*3:(row+1)*3]) + ' |')

    def make_move(self, move, player):
        """Makes a move on the board. Marks the square with 'X' for first player and 'O' for second player."""
        letter = 'X' if player == 1 else 'O'
        if self.board[move] == ' ':
            self.board[move] = letter
            if self.winner(move, letter):
                self.current_winner = player
            return True
        return False

    def undo_move(self, move):
        """Reverts a move on the board."""
        self.board[move] = ' '
        self.current_winner = None

    def get_available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def is_game_over(self):
        return self.current_winner is not None or not self.empty_squares()

    def evaluate_game_state(self, player):
        if self.current_winner:
            # Las condiciones existentes se manejan aquí
            return 1 if (self.current_winner == player) else -1
        else:
            return 0

    def winner(self, square, letter):
        """Checks if the current move leads to a win."""
        row_ind, col_ind = square // 3, square % 3

        # Check row, column, and diagonals
        row_win = all(self.board[row_ind*3 + i] == letter for i in range(3))
        col_win = all(self.board[col_ind + i*3] == letter for i in range(3))
        diag_win = all(self.board[i] == letter for i in [0, 4, 8]) or all(self.board[i] == letter for i in [2, 4, 6])

        return row_win or col_win or (square % 2 == 0 and diag_win)

    def empty_squares(self):
        return ' ' in self.board
