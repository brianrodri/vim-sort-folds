#!/usr/bin/env python3
# encoding: utf-8
"""Sort folds based on their first line.

Maintainer:	Brian Rodriguez
"""
import contextlib
import itertools
import operator
import vim

__all__ = ['sort_folds']
__version__ = '0.1.1'


class Fold():
    """Represents a foldable sequence of lines in the current buffer.

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
            IndexError: When start_line_num is greater than end_line_num.
        """
        if start_line_num > end_line_num:
            raise IndexError(f'start must be greater than end, but got: '
                             f'start={start_line_num} and end={end_line_num}')
        self.start = start_line_num - 1
        self.end = end_line_num - 1

    def __len__(self):
        return self.end - self.start

    def __getitem__(self, i):
        if 0 <= i < len(self):
            return vim.current.buffer[self.start + i]
        raise IndexError(f'index={i} not in range: [{self.start}, {self.end})')

    def __repr__(self):
        return 'Fold(' + '\n\t'.join(repr(line) for line in self) + ')'


def sort_folds(line_num_key=1):
    """Sorts the folds enclosed by the current range.

    Args:
        line_num_key: int. The line number used to give folds their ordering.
    """
    initial_buf = list(vim.current.buffer)
    initial_folds = list(Fold(*r) for r in get_fold_ranges_in_current_range())
    sorted_folds = sorted(initial_folds, key=operator.itemgetter(0))

    for dst, src in reversed(list(zip(initial_folds, sorted_folds))):
        vim.current.buffer[dst.start:dst.end] = initial_buf[src.start:src.end]
    vim.command('normal! zx')


def get_fold_ranges_in_current_range():
    """Yields the fold ranges found within the current range.

    Yields:
        (int, int). The starting (inclusive) and ending (exclusive) line numbers
            of a fold.
    """
    with restore_cursor():
        next_fold_start = move_to_first_fold_of_range()
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


def move_to_first_fold_of_range():
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
    with restore_cursor():
        containing_fold_level = fold_level(perform_motion('[z'))
    if fold_level(fold_start) == containing_fold_level:
        perform_motion('[z')
    if vim.current.range.start <= fold_start < vim.current.range.end:
        return fold_start
    return None


@contextlib.contextmanager
def restore_cursor():
    """Context manager to restore the cursor's position after closing."""
    initial_cursor = vim.current.window.cursor
    try:
        yield
    finally:
        vim.current.window.cursor = initial_cursor


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
