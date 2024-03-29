import copy

from game import Game
from games.games_utils import adjust_start_position, create_action_dict, is_bigger_piece


class Boop(Game):
    # Constants for types of turns and movements in the game.
    PLACE_CAT = 'Place Cat'
    CHANGE_CATS = 'Change Cats'
    MOVE_S = "Move Small"
    MOVE_B = "Move Big"
    CHANGE = "Change"

    LETTER_DICT = {'a': (1, 'small'),
                   'A': (1, 'big'),
                   'b': (2, 'small'),
                   'B': (2, 'big')}

    PLAYER_DICT = {(1, 'small'): 'a',
                   (1, 'big'): 'A',
                   (2, 'small'): 'b',
                   (2, 'big'): 'B'}

    # Instructions for user input.
    HOW_TO_USE = ("Commands should be:\n"
                  "- 'ms XY' to move a small piece to position (X,Y). Example: 'ms 12' for position (1,2).\n"
                  "- 'mb XY' to move a big piece to position (X,Y). Example: 'mb 42' for position (4,2).\n"
                  "- 'c1 XY' to change a small piece to a big piece at position (X,Y). "
                  "Example: 'c1 33' for position (3,3).\n"
                  "- 'c3 XYXYXY' to change three small pieces to big pieces at positions (X,Y), (X,Y), (X,Y). "
                  "Example: 'c3 232425' for positions (2,3), (2,4), (2,5).\n"
                  "Note: X and Y should be single-digit numbers.")

    def __init__(self):
        """
        Initialize the Boop game with an empty board and setup initial game state.
        """
        self.board = [[' ' for _ in range(6)] for _ in range(6)]
        self.current_player = 1
        self.winner = None
        self.previous_state = None
        self.player_pieces = {
            1: {'small': 8, 'big': 0, 'played_small': [], 'played_big': []},
            2: {'small': 8, 'big': 0, 'played_small': [], 'played_big': []}
        }
        self.next_states = [create_action_dict(1, Boop.PLACE_CAT, [])]
        self.track_previous_state = True

    def game_name(self):
        """
        Return the name of the game.
        """
        return "Boop"

    def get_current_player(self):
        """
        Get the current player's number.
        """
        return self.current_player

    def get_winner(self):
        """
        Get the winner of the game, if there is one.
        """
        return self.winner

    def process_user_input(self, user_input):
        """
        Process user input and return the corresponding move.

        Parameters:
            user_input (str): The user's input command.

        Returns:
            tuple: A tuple representing the move type and associated positions.

        Raises:
            ValueError: If the input format is incorrect or coordinates are not numbers.
        """
        parts = user_input.split()

        if len(parts) < 2:
            raise ValueError("Invalid format. Include an action and a coordinate\n" + Boop.HOW_TO_USE)

        action, coordinates = parts[0], parts[1]

        if not coordinates.isdigit():
            raise ValueError("Coordinates should be numbers")

        if action == "ms" and len(coordinates) == 2:
            return Boop.MOVE_S, [(int(coordinates[0]), int(coordinates[1]))]
        elif action == "mb" and len(coordinates) == 2:
            return Boop.MOVE_B, [(int(coordinates[0]), int(coordinates[1]))]
        elif action == "c1" and len(coordinates) == 2:
            return Boop.CHANGE, [(int(coordinates[0]), int(coordinates[1]))]
        elif action == "c3" and len(coordinates) == 6:
            pos_list = [(int(coordinates[i]), int(coordinates[i + 1])) for i in range(0, len(coordinates), 2)]
            return Boop.CHANGE, pos_list
        else:
            raise ValueError(f"Invalid format. {Boop.HOW_TO_USE}")

    def copy(self, track_previous_state=True):
        new_game = Boop()
        new_game.board = [row[:] for row in self.board]
        new_game.current_player = self.current_player
        new_game.winner = self.winner
        new_game.player_pieces = copy.deepcopy(self.player_pieces)  # Deep copy
        new_game.next_states = copy.deepcopy(self.next_states)  # Deep copy

        new_game.track_previous_state = track_previous_state
        if track_previous_state and self.previous_state:
            new_game.previous_state = self.previous_state.copy()
        else:
            new_game.previous_state = None

        return new_game

    def print_board(self):
        """
        Prints the current state of the game board in a readable format.
        Displays the board with the positions of the pieces and shows the remaining pieces for each player.
        """
        # Print the board with row and column headers
        print('    0   1   2   3   4   5')
        for i, row in enumerate(self.board):
            print(f"{i} | " + ' | '.join(row) + ' |')
        print()

        # Retrieve and calculate the number of remaining pieces for each player
        player_pieces_1 = self.player_pieces[1]
        player_pieces_2 = self.player_pieces[2]

        n_a = player_pieces_1['small'] - len(player_pieces_1['played_small'])
        n_b = player_pieces_2['small'] - len(player_pieces_2['played_small'])
        n_A = player_pieces_1['big'] - len(player_pieces_1['played_big'])
        n_B = player_pieces_2['big'] - len(player_pieces_2['played_big'])

        # Print the remaining pieces and the current winner (if any)
        print(f'Rest of pieces-> a: {n_a}, A: {n_A}, b: {n_b}, B: {n_B}')
        print(f'Current winner: {self.winner}')

    def get_player_positions(self, player):
        """
        Retrieves all positions (both small and big pieces) for a given player.

        Parameters:
            player (int): The player number (1 or 2).

        Returns:
           list: A combined list of tuples representing the positions of both small and big pieces for the player.
        """
        player_data = self.player_pieces[player]
        combined_positions = player_data['played_small'] + player_data['played_big']

        return combined_positions

    def make_move(self, move):
        """
        Executes a given move in the game. This can be either placing a cat on the board or changing cats.

        Parameters:
            move (tuple): Contains the type of move and the positions associated with the move.

        Returns:
            bool: True if the move is successfully executed, False otherwise.
        """

        # Check if the move is valid
        available_moves = self.get_available_moves()
        if move not in available_moves:
            print(f'Move: {move} not in available moves: {available_moves}')
            return False

        # Save the current state for potential undo functionality
        if self.track_previous_state:
            self.previous_state = self.copy()

        # Extract move type and positions
        mov_type, positions = move
        current_state = self.next_states.pop(0)

        # Check if it's a normal move (placing a cat) or a change move
        if current_state["type"] == Boop.PLACE_CAT:
            # Execute a normal move
            row, col = positions[0]
            size = 'small' if mov_type == Boop.MOVE_S else 'big'
            self.make_normal_move(row, col, size)
        else:
            # Execute a change cats move
            self.make_change_cats_move(positions)

        # Update the current player if the game is not over
        if not self.is_game_over():
            self.current_player = self.next_states[0]["player"]

        return True

    def make_change_cats_move(self, positions):
        """
        Executes the move to change cats on the board. This can be either changing one cat or multiple cats.
        Instead of receiving a move type, it directly receives the positions of the cats to be upgraded.

        Parameters:
            positions (list of tuples): A list of tuples where each tuple represents the row and column of a
            cat to be upgraded.
        """

        # Process each position to upgrade the cat
        for position in positions:
            self.upgrade_one_cat(*position)  # Unpack the tuple directly into row and col

    def upgrade_one_cat(self, row, col):
        """
        Upgrades a single cat from small to big, adjusting the counts of small and big pieces accordingly.

        Parameters:
            row (int): The row of the cat to upgrade.
            col (int): The column of the cat to upgrade.
        """
        letter = self.board[row][col]

        # Determine the player number and size based on the letter
        player, size = Boop.LETTER_DICT[letter]
        self.player_pieces[player][f'played_{size}'].remove((row, col))

        # Remove the small cat from the board
        self.board[row][col] = ' '

        # Update the counts of small and big pieces for the respective player
        # Only if the piece is a small piece (lowercase letter)
        if letter.islower():
            self.player_pieces[player]['small'] -= 1
            self.player_pieces[player]['big'] += 1

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
        letter = Boop.PLAYER_DICT[(self.current_player, size)]
        self.board[row][col] = letter
        self.player_pieces[self.current_player][f'played_{size}'].append((row, col))

        # Shift adjacent pieces and check for wins or changes
        self.shift_adjacent_pieces(row, col)
        self.process_results(self.get_player_positions(self.current_player))

        # Update the next states based on current game status
        self.update_next_states()

    def process_results(self, positions):
        """
        Processes the results of shifting pieces, checking for wins or necessary changes.
        Evaluates each position of the current player's pieces for potential winning conditions
        or the need for changes, such as upgrading small pieces to big ones.
        """
        winner = False
        possible_changes = []

        current_player_pieces = self.player_pieces[self.current_player]
        played_pieces_count = len(current_player_pieces['played_small']) + len(current_player_pieces['played_big'])

        if played_pieces_count >= 3:
            result = self.check_number_pieces()
            winner = result == 'WIN'

            if result == 'CHANGE_1':
                possible_changes.append((result, []))

            three_changes = []
            if not winner:
                for pos in positions:
                    three_result = self.check_three(pos, played_pieces_count)
                    if three_result[0] == 'WIN':
                        winner = True
                    elif three_result[0] == 'CHANGE_3':
                        for change_vec in three_result[1]:
                            if change_vec not in three_changes:
                                three_changes.append(change_vec)

            if three_changes:
                possible_changes.append(('CHANGE_3', three_changes))

        self.update_game_status(winner, possible_changes)

    def update_game_status(self, winner, changes):
        """
        Updates the game status based on the results of the last move.

        Parameters:
            winner (bool): Indicates whether the current player has won.
            changes (list): List of possible changes for the current player.

        Description:
        - If there is a winner, updates the winner of the game.
        - If no winner but there are changes, prepares the next state changes.
        """
        if winner:
            self.winner = self.current_player
        else:
            self.prepare_next_state_changes(changes)

    def prepare_next_state_changes(self, changes):
        """
        Prepares the next state changes based on the current game status.
        Handles scenarios for single and multiple cat changes.

        Parameters:
            changes (list): List of changes to process for the current player.

        Description:
        - Processes the changes and either makes the change directly (if only one option)
          or updates the next_states for the player to choose from (if multiple options).
        """
        change_options = []
        # Separate processing for single and multiple cat changes
        for change in changes:
            change_type, change_positions = change
            if change_type == 'CHANGE_1':
                # For single cat changes, find all positions of the specified letter and prepare change moves
                change1_pos = self.get_player_positions(self.current_player)
                change_options.extend([[pos] for pos in change1_pos])
            else:
                change_options.extend(change_positions)

        # If there's only one change move, execute it directly
        if len(change_options) == 1:
            self.make_change_cats_move(change_options[0])
        # If there are multiple change moves, add them to the next states
        elif len(change_options) > 1:
            next_state = create_action_dict(self.current_player, Boop.CHANGE_CATS, change_options)
            self.next_states.append(next_state)

    def update_next_states(self):
        """
        Updates the next_states attribute based on the current state of the game.
        """
        player = 1 if self.current_player == 2 else 2
        next_turn = create_action_dict(player, Boop.PLACE_CAT, [])
        self.next_states.append(next_turn)

    def check_number_pieces(self):
        """
        Checks the number of pieces for the current player on the board to determine game status.
        Determines if the current player has won, if a change of pieces from small to big is needed, or if no special action is required.

        Returns:
            str: A string indicating the game status: 'WIN' if all big pieces are placed,
                 'CHANGE_1' if the total count of small and big pieces is 8, or 'NOTHING' otherwise.
        """
        player_pieces = self.player_pieces[self.current_player]

        # If a player has placed all big pieces on the board, it's a win
        if len(player_pieces['played_big']) == 8:
            return 'WIN'

        # If the combined count of small and big pieces reaches 8, it's time to change small to big pieces
        elif len(player_pieces['played_small']) + len(player_pieces['played_big']) == 8:
            return 'CHANGE_1'

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
        """

        played_letter = self.board[row][col]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Shift each adjacent piece if it's smaller than the played piece
        shifted_pieces = [self.shift_piece(row + dr, col + dc, dr, dc)
                          for dr, dc in directions
                          if 0 <= row + dr < 6 and 0 <= col + dc < 6
                          and self.board[row + dr][col + dc] != ' '
                          and is_bigger_piece(played_letter, self.board[row + dr][col + dc])]

        return

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
            player, size = Boop.LETTER_DICT[fallen_piece]
            self.board[row][col] = ' '
            self.player_pieces[player][f'played_{size}'].remove((row, col))
            return None

        # Case when the target position is empty on the board
        elif self.board[target_row][target_col] == ' ':
            shifted_piece = self.board[row][col]
            player, size = Boop.LETTER_DICT[shifted_piece]
            self.board[target_row][target_col] = self.board[row][col]
            self.player_pieces[player][f'played_{size}'].remove((row, col))
            self.player_pieces[player][f'played_{size}'].append((target_row, target_col))
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
            self.player_pieces = previous_state.player_pieces
            self.next_states = previous_state.next_states

    def check_three(self, position, n_pieces):
        """
        Checks if the last move leads to a win, a change, or neither.
        Evaluates lines (rows, columns, diagonals) from the last move for three consecutive cats.

        Returns:
            A tuple indicating either a win, a change of three small cats to big cats, or none.
            For wins and changes, it also returns the positions of the cats involved.
        """
        row, col = position
        max_count = 3
        possible_changes = []

        # Optimization:
        if n_pieces > 4 and not (row in [1, 4] or col in [1, 4]):
            return 'NOTHING'

        # Check all directions from the last move: rows, columns, diagonals
        directions = [
            (0, 1),  # Row
            (1, 0),  # Column
            (1, 1),  # Diagonal down-right
            (1, -1)  # Diagonal down-left
        ]

        for dr, dc in directions:
            start_row, start_col = adjust_start_position(row, col, dr, dc, max_count)
            result = self.has_three_in_line(start_row, start_col, dr, dc, max_count)

            if result[0] == 'WIN':
                return result
            elif result[0] == 'CHANGE_3':
                if result[1] not in possible_changes:
                    possible_changes.extend(result[1])

        if possible_changes:
            return 'CHANGE_3', possible_changes
        return 'NOTHING'

    def has_three_in_line(self, start_row, start_col, delta_row, delta_col, max_count):
        """Checks a line for a three-in-line condition. Evaluates both small and big cats.
        If three big cats are in line, it's a win. If three cats in line but not all are big,
        it marks a possible change from small to big cats."""
        count = 0
        big_count = 0
        three_pos = []
        possible_changes = []
        letter = Boop.PLAYER_DICT[(self.current_player, 'small')]

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
                            return 'WIN', three_pos  # Win condition with all big cats
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
            return 'CHANGE_3', possible_changes
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
        if state["type"] == Boop.PLACE_CAT:

            player_number = state["player"]
            small_pieces_count = self.player_pieces[player_number]['small']
            small_pieces_in_board = len(self.player_pieces[player_number]['played_small'])
            big_pieces_count = self.player_pieces[player_number]['big']
            big_pieces_in_board = len(self.player_pieces[player_number]['played_big'])

            for space in self.get_available_spaces():
                # Check if small pieces are available and append move
                if small_pieces_count - small_pieces_in_board > 0:
                    available_moves.append((Boop.MOVE_S, [space]))
                # Check if big pieces are available and append move
                if big_pieces_count - big_pieces_in_board > 0:
                    available_moves.append((Boop.MOVE_B, [space]))
        else:
            # If it's not a turn to put a cat, use the moves from the current state
            available_moves = [(Boop.CHANGE, option) for option in state["options"]]

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
            opponent = 1 if player == 2 else 1
            player_pieces = self.player_pieces[player]
            opponent_pieces = self.player_pieces[opponent]

            player_points = 0.05 * (len(player_pieces['played_big']) + player_pieces['big'])
            opponent_points = 0.05 * (len(opponent_pieces['played_big']) + opponent_pieces['big'])

            return player_points - opponent_points

    def next_player(self):
        self.current_player = 2 if self.current_player == 1 else 1
