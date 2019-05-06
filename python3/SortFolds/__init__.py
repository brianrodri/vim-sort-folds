#!/usr/bin/env python3
# encoding: utf-8
"""Sort folds based on their first line.

Maintainer:	Brian Rodriguez
"""
import contextlib
import operator
import vim

__all__ = ['sort_folds']
__version__ = '0.1.1'


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
        """
        self.start = start_line_num - 1
        self.end = end_line_num - 1

    def __getitem__(self, i):
        return vim.current.buffer[self.start + i]


def sort_folds(line_num):
    """Sorts folds enclosed in the current range.

    Args:
        line_num: int. The line number used to give folds their ordering.
    """
    buf = list(vim.current.buffer)
    folds = list(Fold(*r) for r in get_fold_ranges())
    sorted_folds = sorted(folds, key=operator.itemgetter(line_num - 1))

    for dst, src in reversed(list(zip(folds, sorted_folds))):
        vim.current.buffer[dst.start:dst.end] = buf[src.start:src.end]
    vim.command('normal! zx')


def get_fold_ranges():
    """Yields the fold ranges found within the current range.

    Yields:
        tuple(int, int). The starting (inclusive) and ending (exclusive) line
            numbers of a fold.
    """
    with new_cursor_scope():
        next_fold_start = perform_motion_to_first_fold()
        if next_fold_start is None:
            return
        while next_fold_start < vim.current.range.end:
            vim.command('normal! zo')
            fold_start = next_fold_start
            fold_end = perform_motion(']z') + 1
            yield (fold_start, fold_end)

            next_fold_start = perform_motion('zj')
            if (next_fold_start == fold_start or
                    fold_level(next_fold_start) != fold_level(fold_start)):
                break


def perform_motion_to_first_fold():
    """Places the cursor at the first fold in the current range.

    Returns:
        int or None. The line number of the cursor, or None if no folds are
            enclosed by the range.
    """
    fold_start = perform_motion(None)
    if not fold_level(fold_start):
        fold_start = perform_motion('zj')
    if not fold_level(fold_start):
        return None

    vim.command('normal! zo')
    with new_cursor_scope():
        outer_level = fold_level(perform_motion('[z'))
    perform_motion('[z' if fold_level(fold_start) == outer_level else None)

    if vim.current.range.start <= fold_start < vim.current.range.end:
        return fold_start
    return None


@contextlib.contextmanager
def new_cursor_scope():
    """Context manager to restore the cursor's position after closing."""
    cursor = vim.current.window.cursor
    try:
        yield
    finally:
        vim.current.window.cursor = cursor


def perform_motion(motion):
    """Applies the given motion on the cursor.

    Args:
        motion: str or None. The motion to perform.

    Returns:
        int. The line number the cursor ends up in.
    """
    if motion is not None:
        vim.command(f'normal! {motion}')
    return int(vim.eval('line(".")'))


def fold_level(line_num):
    """Returns the fold level at the given line number."""
    return int(vim.eval(f'foldlevel({line_num})'))
