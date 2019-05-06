#!/usr/bin/env python3
# encoding: utf-8
"""Sort folds based on their first line.

Maintainer:	Brian Rodriguez
"""
import itertools
import operator
import vim

__all__ = ['sort_folds']
__version__ = '0.1.1'


class Fold():
    """Iterable representation of a folded sequence of lines in the current
    buffer.

    Attributes:
        start: int. The buffer index at which the fold starts (inclusive).
        end: int. The buffer index at which the fold ends (exclusive).
    """

    def __init__(self, start, end):
        """Initializes a new Fold from the given pair of line numbers.

        Args:
            start: int. The line number at which the fold starts (inclusive).
            end: int. The line number at which the fold ends (exclusive).
        """
        self.start = start - 1
        self.end = end - 1

    def __getitem__(self, i):
        return vim.current.buffer[self.start + i]


def sort_folds(key_line=1):
    """Sorts the folds intersecting the current range.

    Args:
        key_line: int. The line number used to give folds an ordering.
    """
    old_buffer = vim.current.buffer[:]
    old_folds = list(get_folds_intersecting_current_range())
    sorted_folds = sorted(old_folds, key=operator.itemgetter(key_line - 1))
    for old, new in reversed(list(zip(old_folds, sorted_folds))):
        vim.current.buffer[old.start:old.end] = old_buffer[new.start:new.end]


def get_folds_intersecting_current_range():
    """Yields all folds intersecting the currently selected range."""
    starts, ends = (
        itertools.tee(get_start_lines_of_folds_intersecting_current_range()))
    next(ends, None)
    return (Fold(start, end) for start, end in zip(starts, ends))


def get_start_lines_of_folds_intersecting_current_range():
    """Yields starting line numbers of all folds intersecting the current range.

    Yields:
        int.
    """
    old_cursor = vim.current.window.cursor
    fold_head = vim.current.range.start
    while fold_head < vim.current.range.end:
        yield fold_head
        next_fold_head = move_cursor('zj')
        if fold_head < next_fold_head:
            fold_head = next_fold_head
        else:
            fold_head = move_cursor(']z') + 1
            break
    yield fold_head
    vim.current.window.cursor = old_cursor


def move_cursor(motion):
    """Applies a normal command then returns line number the cursor ends up at.

    Args:
        motion: str. When empty, no motion is made.

    Returns:
        int. The line number of the cursor after applying the motion.
    """
    if motion:
        vim.command(f'normal! {motion}')
    return int(vim.eval('line(".")'))
