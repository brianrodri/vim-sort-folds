#!/usr/bin/env python3
# encoding: utf-8
"""Sort vim folds based on their first lines."""
import vim

from sort_folds import cursor
from sort_folds import fold

__all__ = ['sort_folds']
__version__ = '0.3.0'


def sort_folds(line_index_key=0):
    """Sorts the folds intersecting vim's current range.

    Args:
        line_index_key: int. Index of line to use as a fold's comparison key.
    """
    folds = [fold.VimFold(fstart, fend) for fstart, fend in cursor.walk_folds()]
    if len(folds) > 1:
        initial_buffer = vim.current.buffer[:]
        sorted_folds = sorted(folds, key=make_fold_key(line_index_key))
        safe_folds_to_swap = reversed(list(zip(folds, sorted_folds)))
        for old_fold, new_fold in safe_folds_to_swap:
            old_fold[vim.current.buffer] = new_fold[initial_buffer]
        present_result()


def make_fold_key(line_index_key):
    """Returns a key function used to sort VimVolds.

    Args:
        line_index_key: int. Index of line to use as a fold's comparison key.

    Returns:
        callable(VimFold) -> Comparable.
    """
    return (lambda fold: fold.get(line_index_key).lower())


@cursor.CursorRestorer()
def present_result():
    """Modifies vim's fold level to show the sorting results."""
    level = cursor.fold_level(cursor.perform_motion('zXzC')) - 1
    if level > 0:
        vim.command(f'normal! {level}zo')
