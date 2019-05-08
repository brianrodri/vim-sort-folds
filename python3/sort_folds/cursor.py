#!/usr/bin/env python3
"""Utility classes and functions for working with vim's cursor."""
import contextlib
import vim  # pylint: disable=import-error


class CursorRestorer(contextlib.ContextDecorator):
    """Context manager which restores vim's cursor position at exit."""

    def __init__(self):
        self._initial_cursor = None

    def __enter__(self):
        self._initial_cursor = vim.current.window.cursor

    def __exit__(self, *unused_exc_info):
        vim.current.window.cursor = self._initial_cursor


def walk_folds():
    """Yields ranges of line numbers enclosing the folds in vim's current range.

    Yields:
        tuple(int, int). The starting (inclusive) and ending (exclusive) line
            numbers of a fold.
    """
    cursor = move_to_first_fold()
    while cursor is not None and is_in_current_vim_range(cursor):
        fold_start, fold_end, cursor = (
            cursor, perform_motion('zo]z') + 1, perform_motion('zj'))
        if (motion_failed(cursor, fold_start) or
                fold_level(cursor) != fold_level(fold_start)):
            cursor = None
        yield (fold_start, fold_end)


def move_to_first_fold():
    """Places vim's cursor at the first fold intersecting vim's current range.

    Returns:
        int or None. Line number to the beginning of the first fold intersecting
            vim's current range, or None if no such fold exists.
    """
    cursor = perform_motion(None)
    if not fold_level(cursor):
        next_fold_start = perform_motion('zj')
        if motion_failed(cursor, next_fold_start):
            return None
        cursor = next_fold_start
    else:
        with CursorRestorer():
            prev_fold_start = perform_motion('zo[z')
        if (not motion_failed(cursor, prev_fold_start) and
                fold_level(cursor) == fold_level(prev_fold_start)):
            cursor = prev_fold_start
    return cursor if is_in_current_vim_range(cursor) else None


def perform_motion(motion):
    """Moves vim's cursor according to the given motion.

    Args:
        motion: str or None. The motion to perform.

    Returns:
        int. The line number of the cursor after moving.
    """
    if motion is not None:
        vim.command(f'normal! {motion}')
    return int(vim.eval('line(".")'))


def motion_failed(cursor_from, cursor_to):
    """Returns whether a motion failed.

    We can tell if a vim motion failed by checking whether the cursor position
    has changed.

    Args:
        cursor_from: int.
        cursor_to: int.

    Returns:
        bool.
    """
    return cursor_from == cursor_to


def fold_level(line_num):
    """Returns the fold level of the given line number.

    Args:
        line_num: int.

    Returns:
        int. The fold level of the given line number.
    """
    return int(vim.eval(f'foldlevel({line_num})'))


def is_in_current_vim_range(line_num):
    """Returns whether the given line number is enclosed by vim's current range.

    Args:
        line_num: int.

    Returns:
        bool.
    """
    return vim.current.range.start <= line_num <= vim.current.range.end
