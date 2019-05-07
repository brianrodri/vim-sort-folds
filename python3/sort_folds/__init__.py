#!/usr/bin/env python3
# encoding: utf-8
"""Sort vim folds based on their first line."""
from sort_folds import cursor
from sort_folds import fold
import vim

__all__ = ['sort_folds']
__version__ = '0.3.0'


def sort_folds(line_index_key=0):
    """Sorts the folds which are intersecting vim's current range.

    Args:
        line_index_key: int. Index of line to use as a fold's comparison key.
    """
    with cursor.CursorRestorer():
        folds = [fold.VimFold(start, end) for start, end in cursor.walk_folds()]
    if len(folds) > 1:
        initial_buffer = vim.current.buffer[:]
        sorted_folds = sorted(folds, key=make_fold_key(line_index_key))
        for old_fold, new_fold in reversed(list(zip(folds, sorted_folds))):
            old_fold[vim.current.buffer] = new_fold[initial_buffer]
        present_result()


def make_fold_key(line_index_key):
    """Returns a key function used to sort VimFolds.

    Args:
        line_index_key: int. Index of line to use as the folds' comparison key.

    Returns:
        callable(VimFold) -> Comparable.
    """
    return (lambda fold: fold.get(line_index_key).lower())


def present_result():
    """Modify vim's fold level to show the sorting results."""
    level = cursor.fold_level(cursor.perform_motion('zXzC'))
    if level > 1:
        vim.command(f'normal! {level - 1}zo')
