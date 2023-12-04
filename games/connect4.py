from game import Game


class ConnectFour(Game):
    def __init__(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.current_winner = None
        self.combinations, self.combo_dict = get_four_in_a_row_combinations()

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
        self.update_combinations(move, player)

        if self.check_winner(column, row, player):
            self.current_winner = player
        return True

    def undo_move(self, move):
        column = move
        for row in self.board:
            if row[column] != ' ':
                self.update_combinations(move, None, remove=row[column])
                row[column] = ' '
                break

        self.current_winner = None

    def update_combinations(self, move, player, remove=None):
        column = move
        for row in range(6):
            letter = self.board[row][column]
            if letter != ' ':
                for combo in self.combo_dict[(row, column)]:
                    self.update_combo(combo, player, remove)
                break

    def update_combo(self, combo, player, remove):
        empty_spaces, player1_symbols, player2_symbols = self.combinations[combo]
        if not remove:
            if player == 1:
                player1_symbols += 1
            else:
                player2_symbols += 1
            empty_spaces -= 1
        else:
            if remove == 'X':
                player1_symbols -= 1
            else:
                player2_symbols -= 1
            empty_spaces += 1
        self.combinations[combo] = (empty_spaces, player1_symbols, player2_symbols)

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
            return 1000 if self.current_winner == player else -1000
        else:
            score = 0
            for combo in self.combinations:
                score += self.evaluate_combo(combo, player)
            return score

    def evaluate_combo(self, combo, player):
        empty_spaces, player1_symbols, player2_symbols = self.combinations[combo]

        if (player1_symbols > 0 and player2_symbols > 0) or empty_spaces == 4:
            return 0
        elif player == 1:
            if player1_symbols > 1:
                return (10 * player1_symbols) + empty_spaces
            else:
                return -(10 * player2_symbols) - empty_spaces
        else:
            if player2_symbols > 1:
                return (10 * player2_symbols) + empty_spaces
            else:
                return -(10 * player1_symbols) - empty_spaces


def get_four_in_a_row_combinations():
    combinations = {}
    combo_dict = {}
    for r in range(6):
        for c in range(7):
            if c + 3 < 7:
                combo = [(r, c + i) for i in range(4)]
                add_combo(combo, combinations, combo_dict)
            if r + 3 < 6:
                combo = [(r + i, c) for i in range(4)]
                add_combo(combo, combinations, combo_dict)
            if c + 3 < 7 and r + 3 < 6:
                combo = [(r + i, c + i) for i in range(4)]
                add_combo(combo, combinations, combo_dict)
            if c - 3 >= 0 and r + 3 < 6:
                combo = [(r + i, c - i) for i in range(4)]
                add_combo(combo, combinations, combo_dict)
    return combinations, combo_dict


def add_combo(combo, combinations, combo_dict):
    combo_key = tuple(combo)
    combinations[combo_key] = (4, 0, 0)
    for pos in combo:
        combo_dict.setdefault(pos, []).append(combo_key)
