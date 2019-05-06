#!/usr/bin/env python3
# encoding: utf-8
"""Sort closed folds based on first line.

Maintainer:	Brian Rodriguez
"""
import contextlib
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
        self._start, self._end = start, end

    def __iter__(self):
        yield from vim.current.buffer[self._start:self._end]

    def __len__(self):
        return self._end - self._start

    def __getitem__(self, i):
        return vim.current.buffer[self._start + i]


def sort_folds(key_line_number=0):
    """Sorts closed folds in the current range by the given line."""
    sorted_folds = sorted(get_folds(), key=operator.itemgetter(key_line_number))
    vim.current.range[:] = list(itertools.chain.from_iterable(sorted_folds))


def get_folds():
    """Yields all folds in the currently selected range."""
    start, *remaining_starts = get_fold_starting_positions()
    for end in remaining_starts:
        yield Fold(start, end)
        start = end


def get_fold_starting_positions():
    """Yields the starting line numbers of all folds in the current range."""
    range_start, range_end = vim.current.range.start, vim.current.range.end - 1
    with restore_cursor():
        fold_start = range_start
        while fold_start <= range_end:
            yield fold_start
            vim.command('normal! zj')
            next_fold_start = get_cursor_line_number() - 1
            if fold_start < next_fold_start:
                fold_start = next_fold_start
            else:
                vim.command('normal! ]z')
                yield get_cursor_line_number()
                return
        vim.command('normal! zk')
        yield get_cursor_line_number()


@contextlib.contextmanager
def restore_cursor():
    initial_cursor = vim.current.window.cursor
    try:
        yield
    finally:
        vim.current.window.cursor = initial_cursor

def get_cursor_line_number():
    return int(vim.eval('line(".")'))
