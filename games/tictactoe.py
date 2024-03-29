from game import Game


class TicTacToe(Game):
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 1
        self.winner = None
        self.previous_state = None

    def game_name(self):
        return "TicTacToe"

    def get_current_player(self):
        return self.current_player

    def get_winner(self):
        return self.winner

    def process_user_input(self, user_input):

        if not user_input.isdigit() and len(user_input) != 1:
            raise ValueError("Coordinates should be numbers")

        return int(user_input) - 1

    def copy(self, track_previous_state=True):
        new_game = TicTacToe()
        new_game.board = self.board[:]
        new_game.current_player = self.current_player
        new_game.winner = self.winner
        new_game.previous_state = self.previous_state
        return new_game

    def print_board(self):
        print('***************')
        for row in range(3):
            print('| ' + ' | '.join(self.board[row*3:(row+1)*3]) + ' |')

    def make_move(self, move):
        """Makes a move on the board. Marks the square with 'X' for first player and 'O' for second player."""
        letter = 'X' if self.current_player == 1 else 'O'
        if self.board[move] == ' ':
            self.previous_state = self.copy()
            self.board[move] = letter
            if self.check_winner(move, letter):
                self.winner = self.current_player

            self.current_player = self.next_player()
            return True

        print(f"Available moves are: {self.get_available_moves()}")
        return False

    def undo_move(self):
        """Reverts a move on the board."""
        previous_state = self.previous_state.copy()
        if previous_state:
            self.board = previous_state.board
            self.current_player = previous_state.current_player
            self.winner = previous_state.winner
            self.previous_state = previous_state.previous_state

    def get_available_moves(self):
        return [i for i in [4, 0, 2, 6, 8, 1, 3, 5, 7] if self.board[i] == ' ']

    def is_game_over(self):
        return self.winner is not None or not self.empty_squares()

    def evaluate_game_state(self, player):
        if self.winner:
            return 1 if (self.winner == player) else -1
        else:
            return 0

    def check_winner(self, square, letter):
        """Checks if the current move leads to a win."""
        row_ind, col_ind = square // 3, square % 3

        # Check row, column, and diagonals
        row_win = all(self.board[row_ind*3 + i] == letter for i in range(3))
        col_win = all(self.board[col_ind + i*3] == letter for i in range(3))
        diag_win = all(self.board[i] == letter for i in [0, 4, 8]) or all(self.board[i] == letter for i in [2, 4, 6])

        return row_win or col_win or (square % 2 == 0 and diag_win)

    def empty_squares(self):
        return ' ' in self.board

    def next_player(self):
        if self.current_player == 1:
            return 2
        else:
            return 1
