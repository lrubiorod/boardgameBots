

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
