from game import Game


class Boop(Game):
    def __init__(self):
        self.board = [[' ' for _ in range(6)] for _ in range(6)]
        self.current_player = 1
        self.winner = None
        self.previous_state = None
        self.pieces_count = {'a': 0, 'b': 0}

    def game_name(self):
        return "Boop"

    def get_current_player(self):
        return self.current_player

    def get_winner(self):
        return self.winner

    def copy(self):
        new_game = Boop()
        new_game.board = [row[:] for row in self.board]
        new_game.current_player = self.current_player
        new_game.winner = self.winner
        new_game.previous_state = self.previous_state
        new_game.pieces_count = self.pieces_count.copy()
        return new_game

    def print_board(self):
        print('    0   1   2   3   4   5')
        for i, row in enumerate(self.board):
            print(f"{i} | " + ' | '.join(row) + ' |')
        print()
        print(f'Current winner: {self.winner}')

    def make_move(self, move):
        row, col = move
        current_player_letter = 'a' if self.current_player == 1 else 'b'

        if self.board[row][col] != ' ':
            return False

        self.previous_state = self.copy()

        shifted_pieces = self.shift_adjacent_pieces(row, col)

        self.board[row][col] = current_player_letter
        self.pieces_count[current_player_letter] += 1

        shifted_pieces.append([row, col])
        for m in shifted_pieces:
            winner = self.check_winner(m)
            if winner:
                self.winner = 1 if winner == 'a' else 2

        self.current_player = 2 if self.current_player == 1 else 1

        return True

    def shift_adjacent_pieces(self, row, col):
        shifted_pieces = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            adj_row, adj_col = row + dr, col + dc
            if 0 <= adj_row < 6 and 0 <= adj_col < 6 and self.board[adj_row][adj_col] != ' ':
                new_position = self.shift_piece(adj_row, adj_col, dr, dc)
                if new_position:
                    shifted_pieces.append(new_position)
        return shifted_pieces

    def shift_piece(self, row, col, dr, dc):
        target_row, target_col = row + dr, col + dc
        if not (0 <= target_row < 6 and 0 <= target_col < 6):
            fallen_piece = self.board[row][col]
            self.board[row][col] = ' '
            if fallen_piece in self.pieces_count:
                self.pieces_count[fallen_piece] -= 1
        elif self.board[target_row][target_col] == ' ':
            self.board[target_row][target_col] = self.board[row][col]
            self.board[row][col] = ' '
            return [target_row, target_col]

        return None

    def undo_move(self):
        """Reverts a move on the board."""
        previous_state = self.previous_state.copy()
        if self.previous_state:
            self.board = previous_state.board
            self.current_player = previous_state.current_player
            self.winner = previous_state.winner
            self.previous_state = previous_state.previous_state
            self.pieces_count = previous_state.pieces_count

    def check_winner(self, last_move):
        """Checks if the last move leads to a win."""
        row, col = last_move
        max_count = 3
        letter = self.board[row][col]

        if letter == ' ':
            return None

        if self.pieces_count[letter] == 8:
            return letter

        if self.check_line_winner(row, max(col - (max_count - 1), 0), 0, 1, letter, max_count):
            return letter

        if self.check_line_winner(max(row - (max_count - 1), 0), col, 1, 0, letter, max_count):
            return letter

        for dr, dc in [(1, 1), (1, -1)]:
            start_row = row
            start_col = col
            for _ in range(max_count - 1):
                if 0 <= start_row - dr < 6 and 0 <= start_col - dc < 6:
                    start_row -= dr
                    start_col -= dc
            if self.check_line_winner(start_row, start_col, dr, dc, letter, max_count):
                return letter

        return None

    def check_line_winner(self, start_row, start_col, delta_row, delta_col, letter, max_count):
        """Checks a line for a winning condition."""
        count = 0
        row, col = start_row, start_col
        for _ in range(max_count + 2):
            if 0 <= row < 6 and 0 <= col < 6 and self.board[row][col] == letter:
                count += 1
                if count == max_count:
                    return True
            else:
                count = 0

            row += delta_row
            col += delta_col

        return False

    def get_available_moves(self):
        central_area = {(2, 2), (2, 3), (3, 2), (3, 3)}
        intermediate_area = {(row, col) for row in range(1, 5) for col in range(1, 5)} - central_area

        def classify_move(row, col):
            if (row, col) in central_area:
                return 'central'
            elif (row, col) in intermediate_area:
                return 'intermediate'
            else:
                return 'outer'

        available_moves = [(row, col) for row in range(6) for col in range(6) if self.board[row][col] == ' ']
        moves_classified = {'central': [], 'intermediate': [], 'outer': []}

        for move in available_moves:
            moves_classified[classify_move(*move)].append(move)

        return moves_classified['central'] + moves_classified['intermediate'] + moves_classified['outer']

    def is_game_over(self):
        return self.winner is not None

    def evaluate_game_state(self, player):
        if self.winner:
            return 1 if self.winner == player else -1
        else:
            return 0

    def next_player(self):
        self.current_player = 2 if self.current_player == 1 else 1
