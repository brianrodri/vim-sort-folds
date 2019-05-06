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
    old_folds = list(get_folds_intersecting_current_range())
    sorted_folds = sorted(old_folds, key=operator.itemgetter(key_line - 1))

    old_buffer = list(vim.current.buffer)
    folds_to_swap = list(zip(old_folds, sorted_folds))
    for dst, src in reversed(folds_to_swap):
        vim.current.buffer[dst.start:dst.end] = old_buffer[src.start:src.end]


def get_folds_intersecting_current_range():
    """Yields all folds intersecting the currently selected range."""
    return (
        Fold(s, e) for s, e in get_spans_of_folds_intersecting_current_range())


def get_spans_of_folds_intersecting_current_range():
    """Yields starting line numbers of all folds intersecting the current range.

    Yields:
        int.
    """
    with restore_cursor():
        at_last_fold = False
        next_fold_start = perform_motion(None)
        while not at_last_fold and next_fold_start <= vim.current.range.end:
            fold_start, next_fold_start = next_fold_start, perform_motion('zj')
            if next_fold_start == fold_start:
                at_last_fold = True
            with restore_cursor():
                fold_end = perform_motion('zo' ']z' 'zc' 'zX') + 1
            yield (fold_start, fold_end)


def perform_motion(motion):
    """Applies a motion, then returns the line number the cursor ends up on.

    Args:
        motion: str or None. The vim motion to perform.

    Returns:
        int. The line number of the cursor after applying the motion.
    """
    if motion is not None:
        vim.command(f'normal! {motion}')
    return int(vim.eval('line(".")'))


@contextlib.contextmanager
def restore_cursor():
    """Context manager to restore the cursor's position after closing."""
    old_cursor = vim.current.window.cursor
    try:
        yield
    finally:
        vim.current.window.cursor = old_cursor
