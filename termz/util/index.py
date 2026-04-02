
def next_index(
    current_index: int,
    max_index: int,
    direction: int = 1,
    loop_behavior: bool = True
) -> int:
    """
    Calculates the next index in a list based on the current index,
    the length of the list and the direction of movement.

    Parameters
    ----------
    current_index : int
        The current index in the list.
    max_index : int
        The length of the list.
    direction : int, optional
        The direction of movement
        (1 for forward, -1 for backward).
    loop_behavior : bool, optional
        If True, the index will wrap around when reaching
        the start or end of the list. If False, the index will be
        clamped within the bounds of the list.

    Returns
    -------
    int
        The calculated next index.

    Notes
    -----
    When `loop_behavior` is `True`, the expression
    `(current_index + direction) % length` ensures that the index
    always stays within the valid range from `0` to `length - 1`.
    The modulo operator (%) makes the index "wrap around":

        - If the index moves past the end of the list, it wraps back
          to 0.
        - If the index moves before the beginning, it wraps to the
        last position.

    Examples
    --------
    For a list of length 5 (indices 0 to 4):

    >>> (4 + 1) % 5  # moves from the end to the start
    0
    >>> (0 - 1) % 5  # moves from the start to the end
    4
    >>> (2 + 1) % 5  # normal forward movement
    3
    >>> (2 - 1) % 5  # normal backward movement
    1
    """
    if loop_behavior:
        return (current_index + direction) % max_index

    if direction < 0:
        return max(current_index - 1, 0)
    else:
        return min(current_index + 1, max_index - 1)
