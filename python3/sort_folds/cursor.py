#!/usr/bin/env python3
# encoding: utf-8
"""Provides utility classes/functions for working with vim's current cursor."""
import vim


class CursorRestorer():
    """Context manager to restore vim's cursor position on exit."""
    def __init__(self):
        self.initial_cursor = vim.current.window.cursor
    def __enter__(self):
        pass
    def __exit__(self, *exc_info):
        vim.current.window.cursor = self.initial_cursor


def walk_over_folds():
    """Yields ranges of foldable line numbers while moving vim's cursor.

    Yields:
        tuple(int, int). The starting (inclusive) and ending (exclusive) line
            numbers of a fold.
    """
    cursor = move_to_first_fold()
    is_at_end_of_folds = (cursor is None)
    while not is_at_end_of_folds and cursor in vim.current.range:
        start, end = cursor, perform_motion('zo]z') + 1
        yield (start, end)
        cursor = perform_motion('zj')
        is_at_end_of_folds = (
            cursor == start or get_fold_level(cursor) != get_fold_level(start))


def move_to_first_fold():
    """Places vim's cursor at the first fold intersecting vim's current range.

    Returns:
        int or None. Line number of the first fold or None if no folds exist.
    """
    cursor = perform_motion(None)
    if not get_fold_level(cursor):
        next_fold_start = perform_motion('zj')
        if cursor == next_fold_start:
            return None
        cursor = next_fold_start
    else:
        with CursorRestorer():
            prev_fold_start = perform_motion('zo[z')
        if get_fold_level(cursor) == get_fold_level(prev_fold_start):
            cursor = prev_fold_start
    return cursor if cursor in vim.current.range else None


def perform_motion(motion):
    """Moves vim's cursor according to the given motion.

    Args:
        motion: str or None. The motion to perform.

    Returns:
        int. The line number on which the cursor ends upon.
    """
    if motion is not None:
        vim.command(f'normal! {motion}')
    return int(vim.eval('line(".")'))


def get_fold_level(line_num=None):
    """Returns the fold level for the given line number.

    Args:
        line_num: int or None. The line number to check. When None, the line
            number will default to the cursor's current position.

    Returns:
        int. The fold level for the given line number.
    """
    if line_num is None:
        line_num = perform_motion(None)
    return int(vim.eval(f'foldlevel({line_num})'))
