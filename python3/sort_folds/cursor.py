#!/usr/bin/env python3
# encoding: utf-8
"""Provides utility classes/functions for working with vim's cursor."""
import contextlib
import vim


class CursorRestorer(contextlib.ContextDecorator):
    """Context manager to restore vim's cursor position on exit."""
    def __enter__(self):
        self._initial_cursor = vim.current.window.cursor

    def __exit__(self, *unused_exc_info):
        vim.current.window.cursor = self._initial_cursor


@CursorRestorer()
def walk_folds():
    """Yields ranges of foldable line numbers discovered by vim's cursor.

    Yields:
        tuple(int, int). The starting (inclusive) and ending (exclusive) line
            numbers of a fold.
    """
    cursor = move_to_first_fold()
    while cursor is not None and in_selected_vim_range(cursor):
        fstart, fend, cursor = (
            cursor, perform_motion('zo]z') + 1, perform_motion('zj'))
        if cursor == fstart or fold_level(cursor) != fold_level(fstart):
            cursor = None
        yield (fstart, fend)


def move_to_first_fold():
    """Places vim's cursor at the first fold intersecting vim's current range.

    Returns:
        int or None. Line number of the first fold, or None if no fold is found.
    """
    cursor = perform_motion(None)
    if not fold_level(cursor):
        next_fold_start = perform_motion('zj')
        if cursor == next_fold_start:
            return None
        else:
            cursor = next_fold_start
    else:
        with CursorRestorer():
            prev_fold_start = perform_motion('zo[z')
        if fold_level(cursor) == fold_level(prev_fold_start):
            cursor = prev_fold_start
    return cursor if in_selected_vim_range(cursor) else None


def perform_motion(motion):
    """Moves vim's cursor using the given motion.

    Args:
        motion: str or None. The motion to perform.

    Returns:
        int. The line number of the cursor after the motion.
    """
    if motion is not None:
        vim.command(f'normal! {motion}')
    return int(vim.eval('line(".")'))


def fold_level(line_num):
    """Returns the fold level for the given line number.

    Args:
        line_num: int.

    Returns:
        int. The fold level of the given line number.
    """
    return int(vim.eval(f'foldlevel({line_num})'))


def in_selected_vim_range(line_num):
    """Returns whether the given line number is within vim's current range.

    Args:
        line_num: int.

    Returns:
        bool.
    """
    return vim.current.range.start <= line_num < vim.current.range.end
