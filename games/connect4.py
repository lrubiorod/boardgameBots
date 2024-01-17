from game import Game


class ConnectFour(Game):
    def __init__(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.current_player = 1
        self.winner = None
        self.previous_state = None

    def game_name(self):
        return "Connect4"

    def get_current_player(self):
        return self.current_player

    def get_winner(self):
        return self.winner

    def process_user_input(self, user_input):

        if not user_input.isdigit() and len(user_input) != 1:
            raise ValueError("Coordinates should be numbers")

        return int(user_input)

    def copy(self, track_previous_state=True):
        new_game = ConnectFour()
        new_game.board = [row[:] for row in self.board]
        new_game.current_player = self.current_player
        new_game.winner = self.winner
        new_game.previous_state = self.previous_state
        return new_game

    def print_board(self):
        print(' 0 1 2 3 4 5 6')
        for row in self.board:
            print('|' + '|'.join(row) + '|')
        print()
        print(f'Current winner: {self.winner}')

    def make_move(self, move):
        column = move
        player = self.current_player

        if self.board[0][column] != ' ':
            return False

        self.previous_state = self.copy()
        row = next(row for row in reversed(self.board) if row[column] == ' ')
        row[column] = 'X' if player == 1 else 'O'

        if self.check_winner(column, row, player):
            self.winner = player

        self.current_player = self.next_player()
        return True

    def undo_move(self):
        """Reverts a move on the board."""
        previous_state = self.previous_state.copy()
        if self.previous_state:
            self.board = previous_state.board
            self.current_player = previous_state.current_player
            self.winner = previous_state.winner
            self.previous_state = previous_state.previous_state

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
        return self.winner is not None or all(self.board[0][i] != ' ' for i in range(7))

    def evaluate_game_state(self, player):
        if self.winner:
            return 1 if self.winner == player else -1
        else:
            return 0

    def next_player(self):
        if self.current_player == 1:
            return 2
        else:
            return 1
