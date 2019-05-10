"""Utility classes and functions for working with vim's cursor."""
import contextlib
import vim  # pylint: disable=import-error


class CursorRestorer(contextlib.ContextDecorator):
    """Restores vim's cursor position on exit."""

    def __init__(self):
        self._initial_cursor = None

    def __enter__(self):
        self._initial_cursor = vim.current.window.cursor

    def __exit__(self, *unused_exc_info):
        vim.current.window.cursor = self._initial_cursor


def walk_folds():
    """Yields pairs of line numbers which enclose a fold in vim's current range.

    Yields:
        tuple(int, int). The starting (inclusive) and stopping (exclusive) line
            numbers of a fold.
    """
    fold_start = move_to_start_of_first_fold()
    while fold_start is not None:
        with CursorRestorer():
            yield (fold_start, perform_motion('zo]z') + 1)
        next_fold_start = perform_motion('zj')
        if (next_fold_start != fold_start
                and in_vim_current_range(next_fold_start)
                and fold_level(next_fold_start) == fold_level(fold_start)):
            fold_start = next_fold_start
        else:
            fold_start = None


def move_to_start_of_first_fold():
    """Places cursor at the start of the first fold within vim's current range.

    Returns:
        int or None. Line number to the start of the first fold, or None if no
            such fold exists.
    """
    cursor = perform_motion(None)
    if fold_level(cursor):
        with CursorRestorer():
            fstart = perform_motion('zo[z')
        if fstart != cursor and fold_level(fstart) == fold_level(cursor):
            return perform_motion('zo[z')
        return cursor
    else:
        with CursorRestorer():
            fstart = perform_motion('zj')
        if fstart != cursor and in_vim_current_range(fstart):
            return perform_motion('zj')
        return None


def perform_motion(motion):
    """Performs the given vim motion.

    Args:
        motion: str or None. The vim motion to perform.

    Returns:
        int. The line number of the cursor after moving.
    """
    if motion is not None:
        vim.command(f'normal! {motion}')
    return int(vim.eval('line(".")'))


def fold_level(line_num):
    """Returns fold level of the given line number.

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
