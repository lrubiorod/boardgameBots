

def adjust_start_position(row, col, delta_row, delta_col, max_count):
    """
    Adjusts the start position for checking lines based on the direction and max count.

    Args:
        row (int): The row position of the last move.
        col (int): The column position of the last move.
        delta_row (int): Row increment for the direction.
        delta_col (int): Column increment for the direction.
        max_count (int): The count of consecutive cats to check for.

    Returns:
        Tuple of adjusted start row and column.
    """
    start_row, start_col = row, col
    for _ in range(max_count - 1):
        if 0 <= start_row - delta_row < 6 and 0 <= start_col - delta_col < 6:
            start_row -= delta_row
            start_col -= delta_col
    return start_row, start_col


def create_action_dict(player, action_type, options):
    """
    Creates a dictionary representing a pending action in the game, particularly useful for actions
    that involve multiple choices, like changing cats. This structure enhances clarity and
    flexibility in handling game decisions.

    Parameters:
        player (int): The player number who is responsible for the action.
        action_type (str): The type of action, e.g., 'Change Cats', 'Place Cat'.
        options (list of lists of tuples): Options available for the action, each option being
                                           a list of positions (tuples) on the board.

    Returns:
        dict: A dictionary representing the pending action with its available options.
    """
    return {
        "player": player,
        "type": action_type,
        "options": options,
    }


def is_bigger_piece(first, second):
    """
    Determines if the first piece is bigger or equal than the second.
    A piece is considered bigger if it's uppercase.
    """
    return first.isupper() or not second.isupper()