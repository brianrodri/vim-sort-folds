#!/usr/bin/env python3
# encoding: utf-8
"""Sort closed folds based on first line.

Maintainer:	Brian Rodriguez
"""
import itertools
import operator
import vim

__all__ = ['sort_folds']
__version__ = '0.1.0'


class Fold():
    """Iterable representation of a folded sequence of lines in the buffer."""

    def __init__(self, start, end):
        """Initializes a new Fold.

        Args:
            start: int. The line number at which the fold starts (inclusive).
            end: int. The line number at which the fold ends (exclusive).

        Raises:
            IndexError: When start > end.
        """
        if start > end:
            raise IndexError(f'start must not be greater than end, but got '
                             f'start={start} and end={end}')
        self._start = start - 1
        self._end = end - 1

    def __len__(self):
        return self._end - self._start

    def __getitem__(self, i):
        return vim.current.buffer[self._start + i]

    @property
    def slice(self):
        """Returns a slice for indexing the folded lines in the buffer."""
        return slice(self._start, self._end, 1)


def sort_folds(key_line_number=0):
    """Sorts closed folds in the current range by the given line."""
    initial_buf = tuple(vim.current.buffer)
    initial_folds = tuple(get_folds())
    sorted_buf = sorted(initial_folds, key=operator.itemgetter(key_line_number))

    # Move sorted folds into the positions of the initial folds.
    for old_fold, new_fold in reversed(tuple(zip(initial_folds, sorted_buf))):
        vim.current.buffer[old_fold.slice] = initial_buf[new_fold.slice]


def get_folds():
    """Yields all folds in the currently selected range."""
    fold_starts, fold_ends = itertools.tee(get_fold_starting_positions())
    next(fold_ends)  # Drop the first fold position.
    yield from (Fold(start, end) for start, end in zip(fold_starts, fold_ends))


def get_fold_starting_positions():
    """Yields the starting line numbers of all folds in the current range."""
    initial_cursor = vim.current.window.cursor
    range_start, range_end = vim.current.range.start, vim.current.range.end + 1
    fold_start = range_begin
    while fold_start < range_end:
        yield fold_start
        vim.command('normal! zj')
        next_fold_start = int(vim.eval('line(".")'))
        if fold_start < next_fold_start:
            fold_start = next_fold_start
        else:
            break  # We've hit the last fold in the buffer.
    yield range_end
    vim.current.window.cursor = initial_cursor
