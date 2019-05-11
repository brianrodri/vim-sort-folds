"""Utility functions for working with vim's cursor."""
import contextlib
import vim  # pylint: disable=import-error


def walk_folds():
    """Yields pairs of line numbers which enclose a fold in vim's current range.

    Yields:
        tuple(int, int). The starting (inclusive) and stopping (exclusive)
            indices of a fold.
    """
    fold_start = move_to_start_of_first_fold()
    while fold_start is not None:
        yield (fold_start - 1, perform_motion('zo' ']z'))
        next_fold_start = perform_motion('zj')
        if (next_fold_start != fold_start
                and fold_level(next_fold_start) == fold_level(fold_start)
                and in_vim_current_range(next_fold_start)):
            fold_start = next_fold_start
        else:
            fold_start = None


def move_to_start_of_first_fold():
    """Places cursor at start of the first fold within vim's current range.

    Returns:
        int or None. Line number to the start of the first fold within vim's
            current range, or None if there isn't one.
    """
    cur_line = line_number()
    if fold_level(cur_line):
        with cursor_restorer():
            parent_fold_start = perform_motion('zo' '[z')
        if fold_level(parent_fold_start) == fold_level(cur_line):
            return perform_motion('zo' '[z')
        return cur_line
    with cursor_restorer():
        first_fold_start = perform_motion('zj')
    if first_fold_start != cur_line and in_vim_current_range(first_fold_start):
        return perform_motion('zj')
    return None


@contextlib.contextmanager
def cursor_restorer():
    """Restores vim's cursor position on exit."""
    cursor_to_restore = vim.current.window.cursor
    try:
        yield
    finally:
        vim.current.window.cursor = cursor_to_restore


def perform_motion(motion):
    """Performs the given vim-motion.

    Args:
        motion: str. The vim-motion to perform.

    Returns:
        int. The line number of the cursor after moving.
    """
    vim.command(f'normal! {motion}')
    return line_number()


def line_number():
    """Returns the line number vim's cursor is currently on.

    Returns:
        int.
    """
    return int(vim.eval('line(".")'))


def fold_level(line_num):
    """Returns the fold-level of the given line number.

    Args:
        line_num: int.

    Returns:
        int.
    """
    return int(vim.eval(f'foldlevel({line_num})'))


def in_vim_current_range(line_num):
    """Returns whether the given line number is within vim's current range.

    Args:
        line_num: int.

    Returns:
        bool.
    """
    return vim.current.range.start <= (line_num - 1) <= vim.current.range.end
