#!/usr/bin/env python3
# encoding: utf-8
"""Sort vim folds based on their first lines."""
import contextlib
import vim

from . import vim_fold

__all__ = ['sort_folds']
__version__ = '0.3.0'


def sort_folds(key_index=0):
    """Sorts the folds intersecting vim's current range.

    Args:
        key_index: int. Which line index to use as the folds' comparison key.
    """
    buffer_copy = vim.current.buffer[:]
    with cursor_restorer():
        initial_folds = [vim_fold.VimFold(*r) for r in walk_over_fold_spans()]
    sorted_folds = sorted(initial_folds, key=lambda f: f.get(key_index).lower())
    safe_folds_to_swap = reversed(list(zip(initial_folds, sorted_folds)))
    for old_fold, new_fold in safe_folds_to_swap:
        old_fold[vim.current.buffer] = new_fold[buffer_copy]
    present_result()


@contextlib.contextmanager
def cursor_restorer():
    """Context manager to restore vim's cursor position after exiting."""
    initial_cursor = vim.current.window.cursor
    try:
        yield
    finally:
        vim.current.window.cursor = initial_cursor


def walk_over_fold_spans():
    """Yields ranges of foldable line numbers while moving vim's cursor.

    Yields:
        tuple(int, int). The starting (inclusive) and ending (exclusive) line
            numbers of a fold.
    """
    cursor = move_to_first_fold()
    at_end_of_folds = (cursor is None)
    while not at_end_of_folds and cursor in vim.current.range:
        start, end = (cursor, perform_motion('zo]z') + 1)
        yield (start, end)
        cursor = perform_motion('zj')
        at_end_of_folds = (
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
        with cursor_restorer():
            prev_fold_start = perform_motion('zo[z')
        if get_fold_level(cursor) == get_fold_level(prev_fold_start):
            cursor = prev_fold_start
    return cursor if cursor in vim.current.range else None


def present_result():
    """Modifies vim's fold level to display the folds that have been sorted."""
    level = get_fold_level(perform_motion('zXzC'))
    if level:
        vim.command(f'normal! {level}zo')


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


def get_fold_level(line_num):
    """Returns the fold level for the given line number.

    Args:
        line_num: int.

    Returns:
        int. The fold level for the given line number.
    """
    return int(vim.eval(f'foldlevel({line_num})'))
