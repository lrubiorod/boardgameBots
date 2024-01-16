import copy

from game import Game
from games.games_utils import adjust_start_position


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
        """
        Makes a normal move by placing a piece on the board, checks for winners,
        and updates game state accordingly.

        Parameters:
            row (int): Row of the move.
            col (int): Column of the move.
            size (str): Size of the piece ('small' or 'big').
        """
        # Determine the letter for the current player's piece
        letter = ('a' if size == 'small' else 'A') if self.current_player == 1 else ('b' if size == 'small' else 'B')
        self.board[row][col] = letter
        self.played_pieces_count[letter] += 1

        # Shift adjacent pieces and check for wins or changes
        shifted_pieces = self.shift_adjacent_pieces(row, col)
        self.process_shift_results(shifted_pieces + [[row, col]], letter)

        # Update the next states based on current game status
        self.update_next_states()

    def process_shift_results(self, positions, letter):
        """
        Processes the results of shifting pieces, checking for wins or necessary changes.
        This function evaluates each shifted position for potential winning conditions or
        the need for changes (like upgrading small pieces to big ones).

        Parameters:
            positions (list): List of positions to check after pieces have been shifted.
            letter (str): The letter representing the player who made the last move.
        """
        # Check the number of pieces on the board for the current player
        result = self.check_number_pieces(letter)
        winner_a, winner_b = result == 'WIN_A', result == 'WIN_B'
        possible_changes_a, possible_changes_b = [], []

        # Append possible changes if a change condition is met
        if result == 'CHANGE_1_A':
            possible_changes_a.append((result, []))
        elif result == 'CHANGE_1_B':
            possible_changes_b.append((result, []))

        # Process each position for potential three-in-line patterns
        if not winner_a or not winner_b:
            for pos in positions:
                three_result = self.check_three(pos)
                if three_result[0] == 'WIN_A':
                    winner_a = True
                elif three_result[0] == 'WIN_B':
                    winner_b = True
                elif three_result[0] == 'CHANGE_3_A':
                    possible_changes_a.append(three_result)
                elif three_result[0] == 'CHANGE_3_B':
                    possible_changes_b.append(three_result)

        self.update_game_status(winner_a, winner_b, possible_changes_a, possible_changes_b)

    def update_game_status(self, winner_a, winner_b, changes_a, changes_b):
        """
        Updates the game status based on the results of the last move.

        Parameters:
            winner_a (bool): Whether player A has won.
            winner_b (bool): Whether player B has won.
            changes_a (list): List of possible changes for player A.
            changes_b (list): List of possible changes for player B.
        """
        if winner_a and winner_b:
            self.winner = 0
        elif winner_a:
            self.winner = 1
        elif winner_b:
            self.winner = 2
        else:
            self.prepare_next_state_changes(changes_a, 'A')
            self.prepare_next_state_changes(changes_b, 'B')

    def prepare_next_state_changes(self, changes, letter):
        """
        Prepares the next state changes based on the current game status.

        Parameters:
            changes (list): List of changes to process.
            letter (str): Letter representing the player ('A' or 'B').
        """
        t = []
        for change in changes:
            if change[0] == f'CHANGE_1_{letter}':
                change1_pos = self.find_letter_positions(letter)
                t.extend([(Boop.CHANGE_1, [pos]) for pos in change1_pos])
            elif change[0] == f'CHANGE_3_{letter}':
                t.extend([(Boop.CHANGE_3, three_pos) for three_pos in change[1]])

        if len(t) == 1:
            self.make_change_cats_move(t[0])
        elif len(t) > 1:
            self.next_states.append((Boop.CHANGE_CATS_A if letter == 'A' else Boop.CHANGE_CATS_B, t))

    def update_next_states(self):
        """
        Updates the next_states attribute based on the current state of the game.
        """
        next_turn = Boop.PUT_CAT_A if self.current_player == 2 else Boop.PUT_CAT_B
        self.next_states.append((next_turn, []))

    def check_number_pieces(self, letter):
        """
        Checks the number of pieces for a specific player on the board to determine game status.
        It determines if a player has won, if a change of pieces (small to big) is needed, or if there is no special action required.

        Parameters:
            letter (str): The letter representing the player (either upper or lower case).

        Returns:
            str: A string indicating the game status: 'WIN', 'CHANGE_1', or 'NOTHING'.
        """

        # If a player has placed all big pieces on the board, it's a win
        if letter.isupper() and (self.played_pieces_count[letter] == 8):
            return f'WIN_{letter.upper()}'

        # If the combined count of small and big pieces reaches 8, it's time to change small to big pieces
        elif self.played_pieces_count[letter.upper()] + self.played_pieces_count[letter.lower()] == 8:
            return f'CHANGE_1_{letter.upper()}'

        # Otherwise, there's no special condition to address
        else:
            return 'NOTHING'

    def shift_adjacent_pieces(self, row, col):
        """
        Shifts adjacent pieces around a given position on the board.
        Only shifts a piece if it's smaller or equal than the played piece.

        Parameters:
            row (int): The row of the played piece.
            col (int): The column of the played piece.

        Returns:
            list: A list of new positions where adjacent pieces were moved.
        """

        def is_bigger_piece(first, second):
            """
            Determines if the first piece is bigger or equal than the second.
            A piece is considered bigger if it's uppercase.
            """
            return first.isupper() or not second.isupper()

        played_letter = self.board[row][col]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Shift each adjacent piece if it's smaller than the played piece
        shifted_pieces = [self.shift_piece(row + dr, col + dc, dr, dc)
                          for dr, dc in directions
                          if 0 <= row + dr < 6 and 0 <= col + dc < 6
                          and self.board[row + dr][col + dc] != ' '
                          and is_bigger_piece(played_letter, self.board[row + dr][col + dc])]

        # Filter out None values (cases where no shift occurred)
        return [pos for pos in shifted_pieces if pos]

    def shift_piece(self, row, col, dr, dc):
        """
        Shifts a piece on the board based on the given direction.
        If the target position is off the board, the piece is removed.
        If the target position is empty, the piece is moved to that position.

        Parameters:
            row (int): The row of the piece to be moved.
            col (int): The column of the piece to be moved.
            dr (int): The row direction of the movement.
            dc (int): The column direction of the movement.

        Returns:
            list or None: The new position [target_row, target_col] if the piece is moved,
                          or None if the piece is removed or no movement is made.
        """
        # Calculate the target position
        target_row, target_col = row + dr, col + dc

        # Case when the target position is off the board
        if not (0 <= target_row < 6 and 0 <= target_col < 6):
            fallen_piece = self.board[row][col]
            self.board[row][col] = ' '
            if fallen_piece in self.played_pieces_count:
                self.played_pieces_count[fallen_piece] -= 1
            return None

        # Case when the target position is empty on the board
        elif self.board[target_row][target_col] == ' ':
            self.board[target_row][target_col] = self.board[row][col]
            self.board[row][col] = ' '
            return [target_row, target_col]

        # No movement is made
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
        """
        Checks if the last move leads to a win, a change, or neither.
        Evaluates lines (rows, columns, diagonals) from the last move for three consecutive cats.

        Returns:
            A tuple indicating either a win, a change of three small cats to big cats, or none.
            For wins and changes, it also returns the positions of the cats involved.
        """
        row, col = last_move
        max_count = 3
        letter = self.board[row][col]

        possible_changes = []

        # Check all directions from the last move: rows, columns, diagonals
        directions = [
            (0, 1),  # Row
            (1, 0),  # Column
            (1, 1),  # Diagonal down-right
            (1, -1)  # Diagonal down-left
        ]

        for dr, dc in directions:
            start_row, start_col = adjust_start_position(row, col, dr, dc, max_count)
            result = self.has_three_in_line(start_row, start_col, dr, dc, letter, max_count)

            if result[0] == f'WIN_{letter.upper()}':
                return result
            elif result[0] == f'CHANGE_3_{letter.upper()}':
                possible_changes.extend(result[1])

        if possible_changes:
            return f'CHANGE_3_{letter.upper()}', possible_changes
        return 'NONE', []

    def has_three_in_line(self, start_row, start_col, delta_row, delta_col, letter, max_count):
        """Checks a line for a three-in-line condition. Evaluates both small and big cats.
        If three big cats are in line, it's a win. If three cats in line but not all are big,
        it marks a possible change from small to big cats."""
        count = 0
        big_count = 0
        three_pos = []
        possible_changes = []

        row, col = start_row, start_col
        for _ in range(max_count + 2):
            if 0 <= row < 6 and 0 <= col < 6:
                this_letter = self.board[row][col]
                if this_letter.lower() == letter.lower():
                    three_pos.append((row, col))
                    count += 1
                    if this_letter.isupper():
                        big_count += 1

                    if count == max_count:
                        if big_count == max_count:
                            return f'WIN_{letter.upper()}', three_pos  # Win condition with all big cats
                        possible_changes.append(three_pos.copy())  # Potential change with small cats
                        r, c = three_pos.pop(0)
                        if self.board[r][c] == letter.upper():
                            big_count -= 1
                        count -= 1
                else:
                    three_pos = []  # Reset if sequence is broken
                    count = big_count = 0

            row += delta_row
            col += delta_col

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
