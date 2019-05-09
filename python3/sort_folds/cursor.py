#!/usr/bin/env python3
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
    cursor = move_to_first_fold()
    while cursor is not None and is_in_current_vim_range(cursor):
        fold_start, fold_stop = (cursor, perform_motion('zo]z') + 1)
        cursor = perform_motion('zj')
        if (motion_failed(cursor, fold_start) or
                fold_level(cursor) != fold_level(fold_start)):
            cursor = None
        yield (fold_start, fold_stop)


def move_to_first_fold():
    """Places cursor at the start of the first fold within vim's current range.

    Returns:
        int or None. Line number to start of the first fold, or None if no such
            fold exists.
    """
    cursor = perform_motion(None)
    if not fold_level(cursor):
        with CursorRestorer():
            next_fold_start = perform_motion('zj')
        if not motion_failed(cursor, next_fold_start):
            cursor = perform_motion('zj')
        else:
            return None
    else:
        with CursorRestorer():
            prev_fold_start = perform_motion('zo[z')
        if (not motion_failed(cursor, prev_fold_start) and
                fold_level(cursor) == fold_level(prev_fold_start)):
            cursor = perform_motion('zo[z')
    return cursor if is_in_current_vim_range(cursor) else None


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


def motion_failed(cursor_start, cursor_stop):
    """Returns whether a given motion failed.

    Args:
        cursor_start: int.
        cursor_stop: int.

    Returns:
        bool.
    """
    # NOTE: Vim's cursor does not move when a motion fails.
    return cursor_start == cursor_stop


def fold_level(line_num):
    """Returns fold level of the given line number.

    Args:
        line_num: int.

    Returns:
        int.
    """
    return int(vim.eval(f'foldlevel({line_num})'))


def is_in_current_vim_range(line_num):
    """Returns whether the given line number is within vim's current range.

    Args:
        line_num: int.

    Returns:
        bool.
    """
    return vim.current.range.start <= line_num <= vim.current.range.end
