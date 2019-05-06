#!/usr/bin/env python3
# encoding: utf-8
"""Sort folds based on their first line.

Maintainer:	Brian Rodriguez
"""
import contextlib
import operator
import vim

__all__ = ['sort_folds']
__version__ = '0.3.0'


class Fold():
    """Encapsulates a folded sequence of lines in the current buffer.

    Attributes:
        start: int. The buffer index at which the fold starts (inclusive).
        end: int. The buffer index at which the fold ends (exclusive).
    """

    def __init__(self, start_line_num, end_line_num):
        """Initializes a new Fold from the given pair of line numbers.

        Args:
            start_line_num: int. Line number where the fold starts (inclusive).
            end_line_num: int. Line number where the fold ends (exclusive).

        Raises:
            IndexError: when end_line_num is less than start_line_num.
        """
        if end_line_num < start_line_num:
            raise IndexError(f'end must not be less than start, but got: '
                             f'end={end_line_num} and start={start_line_num}')
        self.start = start_line_num - 1
        self.end = end_line_num - 1

    def __len__(self):
        return self.end - self.start

    def __getitem__(self, i):
        if 0 <= i < len(self):
            return vim.current.buffer[self.start + i].lower()
        raise IndexError(f'index={i} must be in the range [0, len={len(self)})')


def sort_folds(line_index=0):
    """Sorts folds enclosed in the current range.

    Args:
        line_index: int. The index to the line which gives folds their ordering.
    """
    initial_folds = list(Fold(*r) for r in iter_fold_ranges())
    sorted_folds = sorted(initial_folds, key=operator.itemgetter(line_index))

    initial_buffer, current_buffer = vim.current.buffer[:], vim.current.buffer
    for dst, src in reversed(list(zip(initial_folds, sorted_folds))):
        current_buffer[dst.start:dst.end] = initial_buffer[src.start:src.end]

    # Present the result.
    vim.command('normal! zxzC')
    level = fold_level(perform_motion(None))
    if level > 1:
        vim.command(f'normal! {level}zo')


@contextlib.contextmanager
def cursor_restorer():
    """Context manager to restore the opening cursor position after exiting."""
    initial_cursor = vim.current.window.cursor
    try:
        yield
    finally:
        vim.current.window.cursor = initial_cursor


def iter_fold_ranges():
    """Yields the fold ranges found within the current range.

    Yields:
        tuple(int, int). The starting (inclusive) and ending (exclusive) line
            numbers of a fold.
    """
    with cursor_restorer():
        cursor = move_to_first_fold()
        if cursor is None:
            return
        while cursor < vim.current.range.end:
            vim.command('normal! zo')
            start, end = cursor, perform_motion(']z') + 1
            yield (start, end)

            cursor = perform_motion('zj')
            if cursor == start or fold_level(cursor) != fold_level(start):
                break


def move_to_first_fold():
    """Places the cursor at the first fold within the current range.

    Returns:
        int or None. Line number of the first fold or None if no folds exist.
    """
    cursor = perform_motion(None)
    if not fold_level(cursor):
        cursor = perform_motion('zj')
        if not fold_level(cursor):
            return None

    vim.command('normal! zo')
    with cursor_restorer():
        is_cursor_at_fold_start = (
            fold_level(cursor) != fold_level(perform_motion('[z')))
    perform_motion(None if is_cursor_at_fold_start else '[z')

    if vim.current.range.start <= cursor < vim.current.range.end:
        return cursor
    else:
        return None


def perform_motion(motion):
    """Applies the given motion to the cursor.

    Args:
        motion: str or None. The motion to perform.

    Returns:
        int. The line number the cursor ends up in.
    """
    if motion is not None:
        vim.command(f'normal! {motion}')
    return int(vim.eval('line(".")'))


def fold_level(line_num):
    """Returns the fold level of the given line number.

    Args:
        line_num: int.

    Returns:
        int. The fold-level of the given line number.
    """
    return int(vim.eval(f'foldlevel({line_num})'))
