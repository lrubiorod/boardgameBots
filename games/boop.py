from game import Game
import copy


class Boop(Game):
    PUT_CAT_A = 'Turn A'
    PUT_CAT_B = 'Turn B'
    CHANGE_CATS_A = 'Change Cats A'
    CHANGE_CATS_B = 'Change Cats B'

    # BOOP MOVEMENTS
    MOVE_S = "Move Small"
    MOVE_B = "Move Big"
    CHANGE_1 = "Change 1 cat"
    CHANGE_3 = "Change 3 cats"

    # HOW TO USE
    HOW_TO_USE = ("Commands should be:\n"
                  "- 'ms XY' to move a small piece to position (X,Y). Example: 'ms 12' for position (1,2).\n"
                  "- 'mb XY' to move a big piece to position (X,Y). Example: 'mb 42' for position (4,2).\n"
                  "- 'c1 XY' to change a small piece to a big piece at position (X,Y). "
                  "Example: 'c1 33' for position (3,3).\n"
                  "- 'c3 XYXYXY' to change three small pieces to big pieces at positions (X,Y), (X,Y), (X,Y). "
                  "Example: 'c3 232425' for positions (2,3), (2,4), (2,5).\n"
                  "Note: X and Y should be single-digit numbers.")

    def __init__(self):
        self.board = [[' ' for _ in range(6)] for _ in range(6)]
        self.current_player = 1
        self.winner = None
        self.previous_state = None
        self.small_pieces_player = {1: 8, 2: 8}
        self.big_pieces_player = {1: 0, 2: 0}
        self.played_pieces_count = {'A': 0, 'B': 0, 'a': 0, 'b': 0}
        self.next_states = [(Boop.PUT_CAT_A, [])]

    def game_name(self):
        return "Boop"

    def get_current_player(self):
        return self.current_player

    def get_winner(self):
        return self.winner

    def process_user_input(self, user_input):
        parts = user_input.split()

        if len(parts) < 2:
            raise ValueError("Invalid format. Include an action and a coordinate\n"
                             f"{Boop.HOW_TO_USE}")

        action = parts[0]
        coordinates = parts[1]

        if not coordinates.isdigit():
            raise ValueError("Coordinates should be numbers")

        if action == "ms" and len(coordinates) == 2:
            return Boop.MOVE_S, [(int(coordinates[0]), int(coordinates[1]))]
        elif action == "mb" and len(coordinates) == 2:
            return Boop.MOVE_B, [(int(coordinates[0]), int(coordinates[1]))]
        elif action == "c1" and len(coordinates) == 2:
            return Boop.CHANGE_1, [(int(coordinates[0]), int(coordinates[1]))]
        elif action == "c3" and len(coordinates) == 6:
            pos_list = [(int(coordinates[i]), int(coordinates[i + 1])) for i in range(0, len(coordinates), 2)]
            return Boop.CHANGE_3, pos_list
        else:
            raise ValueError(f"Invalid format. {Boop.HOW_TO_USE}")

    def copy(self):
        new_game = Boop()
        new_game.board = [row[:] for row in self.board]
        new_game.current_player = self.current_player
        new_game.winner = self.winner
        new_game.previous_state = self.previous_state.copy() if self.previous_state else None
        new_game.small_pieces_player = self.small_pieces_player.copy()
        new_game.big_pieces_player = self.big_pieces_player.copy()
        new_game.played_pieces_count = self.played_pieces_count.copy()
        new_game.next_states = copy.deepcopy(self.next_states)  # Deep copy

        return new_game

    def print_board(self):
        print('    0   1   2   3   4   5')
        for i, row in enumerate(self.board):
            print(f"{i} | " + ' | '.join(row) + ' |')
        print()
        n_a = self.small_pieces_player[1] - self.played_pieces_count['a']
        n_b = self.small_pieces_player[2] - self.played_pieces_count['b']
        n_A = self.big_pieces_player[1] - self.played_pieces_count['A']
        n_B = self.big_pieces_player[2] - self.played_pieces_count['B']
        print(f'Rest of pieces-> a: {n_a}, A: {n_A}, b: {n_b}, B: {n_B}')
        print(f'Current winner: {self.winner}')

    def find_letter_positions(self, letter):
        positions = []
        for row in range(6):
            for col in range(6):
                this_letter = self.board[row][col]
                if this_letter.upper() == letter.upper():
                    positions.append((row, col))
        return positions

    def make_move(self, move):
        available_moves = self.get_available_moves()
        if move not in available_moves:
            print(f'Move: {move} not in available moves: {available_moves}')
            return False

        self.previous_state = self.copy()

        mov_type, positions = move
        state = self.next_states.pop(0)

        # Normal movement, putting a cat
        if state[0] == Boop.PUT_CAT_A or state[0] == Boop.PUT_CAT_B:
            row, col = positions[0]
            size = 'small' if mov_type == Boop.MOVE_S else 'big'
            self.make_normal_move(row, col, size)
        else:
            self.make_change_cats_move(move)

        if not self.is_game_over():
            next_state = self.next_states[0]
            if next_state[0] == Boop.PUT_CAT_A or next_state[0] == Boop.CHANGE_CATS_A:
                self.current_player = 1
            else:
                self.current_player = 2

        return True

    def make_change_cats_move(self, move):
        mov_type, positions = move

        if mov_type == Boop.CHANGE_1:
            row, col = positions[0]
            self.upgrade_one_cat(row, col)
        else:
            for (row, col) in positions:
                self.upgrade_one_cat(row, col)

    def upgrade_one_cat(self, row, col):
        letter = self.board[row][col]
        self.played_pieces_count[letter] -= 1

        self.board[row][col] = ' '
        if letter == 'a':
            self.small_pieces_player[1] -= 1
            self.big_pieces_player[1] += 1
        elif letter == 'b':
            self.small_pieces_player[2] -= 1
            self.big_pieces_player[2] += 1

    def make_normal_move(self, row, col, size):
        if size == 'small':
            current_player_letter = 'a' if self.current_player == 1 else 'b'
        else:
            current_player_letter = 'A' if self.current_player == 1 else 'B'

        self.board[row][col] = current_player_letter
        self.played_pieces_count[current_player_letter] += 1

        shifted_pieces = self.shift_adjacent_pieces(row, col)

        possible_changes_a = []
        possible_changes_b = []
        winner_a = False
        winner_b = False
        result = self.check_number_pieces(row, col)
        if result == 'WIN_A':
            winner_a = True
        elif result == 'WIN_B':
            winner_b = True
        elif result == 'CHANGE_1_A':
            possible_changes_a.append((result, []))
        elif result == 'CHANGE_1_B':
            possible_changes_b.append((result, []))

        shifted_pieces.append([row, col])
        for m in shifted_pieces:
            three_result = self.check_three(m)
            if three_result[0] == 'WIN_A':
                winner_a = True
            elif three_result[0] == 'WIN_B':
                winner_b = True
            elif three_result[0] == 'CHANGE_3_A':
                possible_changes_a.append(three_result)
            elif three_result[0] == 'CHANGE_3_B':
                possible_changes_b.append(three_result)

        if winner_a and winner_b:
            self.winner = 0
        elif winner_a and not winner_b:
            self.winner = 1
        elif winner_b and not winner_a:
            self.winner = 2
        else:
            if possible_changes_a:
                t = []
                for change in possible_changes_a:
                    if change[0] == 'CHANGE_1_A':
                        change1_pos = self.find_letter_positions('A')
                        for pos in change1_pos:
                            t.append((Boop.CHANGE_1, [pos]))
                    elif change[0] == 'CHANGE_3_A':
                        for three_pos in change[1]:
                            t.append((Boop.CHANGE_3, three_pos))

                # In case of only one change movement, it makes automatically
                if len(t) == 1:
                    change_move = t[0]
                    self.make_change_cats_move(change_move)
                else:
                    self.next_states.append((Boop.CHANGE_CATS_A, t))

            if possible_changes_b:
                t = []
                for change in possible_changes_b:
                    if change[0] == 'CHANGE_1_B':
                        change1_pos = self.find_letter_positions('B')
                        for pos in change1_pos:
                            t.append((Boop.CHANGE_1, [pos]))
                    elif change[0] == 'CHANGE_3_B':
                        for three_pos in change[1]:
                            t.append((Boop.CHANGE_3, three_pos))

                # In case of only one change movement, it makes automatically
                if len(t) == 1:
                    change_move = t[0]
                    self.make_change_cats_move(change_move)
                else:
                    self.next_states.append((Boop.CHANGE_CATS_B, t))

            next_turn = Boop.PUT_CAT_A if self.current_player == 2 else Boop.PUT_CAT_B
            self.next_states.append((next_turn, []))

        return

    def check_number_pieces(self, row, col):
        letter = self.board[row][col]

        if letter.isupper() and (self.played_pieces_count[letter] == 8):
            return f'WIN_{letter.upper()}'
        elif self.played_pieces_count[letter.upper()] + self.played_pieces_count[letter.lower()] == 8:

            return f'CHANGE_1_{letter.upper()}'
        else:
            return 'NOTHING'

    def shift_adjacent_pieces(self, row, col):

        def is_bigger_piece(first, second):
            if first.isupper():
                return True
            elif second.isupper():
                return False
            else:
                return True

        played_letter = self.board[row][col]
        shifted_pieces = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            adj_row, adj_col = row + dr, col + dc
            if (0 <= adj_row < 6 and 0 <= adj_col < 6 and self.board[adj_row][adj_col] != ' '
                    and is_bigger_piece(played_letter, self.board[adj_row][adj_col])):
                new_position = self.shift_piece(adj_row, adj_col, dr, dc)
                if new_position:
                    shifted_pieces.append(new_position)
        return shifted_pieces

    def shift_piece(self, row, col, dr, dc):
        target_row, target_col = row + dr, col + dc
        if not (0 <= target_row < 6 and 0 <= target_col < 6):
            fallen_piece = self.board[row][col]
            self.board[row][col] = ' '
            if fallen_piece in self.played_pieces_count:
                self.played_pieces_count[fallen_piece] -= 1
        elif self.board[target_row][target_col] == ' ':
            self.board[target_row][target_col] = self.board[row][col]
            self.board[row][col] = ' '
            return [target_row, target_col]

        return None

    def undo_move(self):
        """Reverts a move on the board."""
        previous_state = self.previous_state.copy()
        if previous_state:
            self.board = previous_state.board
            self.current_player = previous_state.current_player
            self.winner = previous_state.winner
            self.previous_state = previous_state.previous_state
            self.small_pieces_player = previous_state.small_pieces_player
            self.big_pieces_player = previous_state.big_pieces_player
            self.played_pieces_count = previous_state.played_pieces_count
            self.next_states = previous_state.next_states

    def check_three(self, last_move):
        """Checks if the last move leads to a win."""
        row, col = last_move
        max_count = 3
        letter = self.board[row][col]

        possible_changes = []

        # Append Row results
        row_result = self.has_three_in_line(row, max(col - (max_count - 1), 0), 0, 1, letter, max_count)
        if row_result[0] == f'WIN_{letter.upper()}':
            return row_result
        elif row_result[0] == f'CHANGE_3_{letter.upper()}':
            for v in row_result[1]:
                possible_changes.append(v)

        # Append Col results
        col_result = self.has_three_in_line(max(row - (max_count - 1), 0), col, 1, 0, letter, max_count)
        if col_result[0] == f'WIN_{letter.upper()}':
            return col_result
        elif col_result[0] == f'CHANGE_3_{letter.upper()}':
            for v in col_result[1]:
                possible_changes.append(v)

        for dr, dc in [(1, 1), (1, -1)]:
            start_row = row
            start_col = col
            for _ in range(max_count - 1):
                if 0 <= start_row - dr < 6 and 0 <= start_col - dc < 6:
                    start_row -= dr
                    start_col -= dc
            # Append diagonal results
            d_result = self.has_three_in_line(start_row, start_col, dr, dc, letter, max_count)
            if d_result[0] == f'WIN_{letter.upper()}':
                return d_result
            elif d_result[0] == f'CHANGE_3_{letter.upper()}':
                for v in d_result[1]:
                    possible_changes.append(v)

        if possible_changes:
            return f'CHANGE_3_{letter.upper()}', possible_changes
        return 'NONE', []  # No three-in-line found

    def has_three_in_line(self, start_row, start_col, delta_row, delta_col, letter, max_count):
        """Checks a line for a three-in-line condition."""
        count = 0
        big_count = 0
        three_pos = []
        possible_changes = []

        for i in range(max_count + 2):
            row, col = start_row + i * delta_row, start_col + i * delta_col
            if not (0 <= row < 6 and 0 <= col < 6):
                three_pos = []  # Start a new sequence
                count = big_count = 0  # Reset the counters
                continue

            this_letter = self.board[row][col]
            if this_letter.lower() == letter.lower():
                three_pos.append((row, col))
                count += 1
                if this_letter.isupper():
                    big_count += 1

                if count == max_count:
                    if big_count == max_count:
                        return f'WIN_{letter.upper()}', three_pos  # All three are big, it's a win

                    possible_changes.append(three_pos.copy())  # Possible change of small cats to big ones
                    r, c = three_pos.pop(0)  # Remove first position
                    if self.board[r][c] == letter.upper():
                        big_count -= 1
                    count -= 1

            else:
                three_pos = []  # Start a new sequence
                count = big_count = 0  # Reset the counters

        if possible_changes:
            return f'CHANGE_3_{letter.upper()}', possible_changes
        return 'NONE', []  # No three-in-line found

    def get_available_moves(self):
        """
        Determines the available moves for the current state of the game.
        If it's a turn to put a cat on the board (either small or big),
        it iterates through available spaces to add possible moves.
        If it's a turn to change cats, it returns the moves available in the current state.
        """
        # If no next states, return an empty list
        if not self.next_states:
            return []

        state = self.next_states[0]
        available_moves = []
        # Check if it's a player's turn to put a cat
        if state[0] in [Boop.PUT_CAT_A, Boop.PUT_CAT_B]:

            player_number = 1 if state[0] == Boop.PUT_CAT_A else 2
            small_pieces_count = self.small_pieces_player[player_number]
            small_pieces_in_board = self.played_pieces_count['a' if player_number == 1 else 'b']
            big_pieces_count = self.big_pieces_player[player_number]
            big_pieces_in_board = self.played_pieces_count['A' if player_number == 1 else 'B']

            for space in self.get_available_spaces():
                # Check if small pieces are available and append move
                if small_pieces_count - small_pieces_in_board > 0:
                    available_moves.append((Boop.MOVE_S, [space]))
                # Check if big pieces are available and append move
                if big_pieces_count - big_pieces_in_board > 0:
                    available_moves.append((Boop.MOVE_B, [space]))
        else:
            # If it's not a turn to put a cat, use the moves from the current state
            available_moves = state[1]

        return available_moves

    def get_available_spaces(self):
        """
        Retrieves a list of available spaces on the board.
        It iterates through the 6x6 board grid, checking for empty spaces.
        An empty space is indicated by ' ' (a space character) in the board array.
        The function returns a list of tuples, where each tuple represents the coordinates
        (row, col) of an available space.
        """
        return [(row, col) for row in range(6) for col in range(6) if self.board[row][col] == ' ']

    def is_game_over(self):
        return self.winner is not None

    def evaluate_game_state(self, player):
        if self.winner:
            return 1 if self.winner == player else -1
        else:
            return 0

    def next_player(self):
        self.current_player = 2 if self.current_player == 1 else 1
