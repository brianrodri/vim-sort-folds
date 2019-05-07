#!/usr/bin/env python3
# encoding: utf-8
"""Sort vim folds based on their first lines."""
import vim

from sort_folds import cursor
from sort_folds import vim_fold

__all__ = ['sort_folds']
__version__ = '0.3.0'


def sort_folds(key_index=0):
    """Sorts the folds intersecting vim's current range.

    Args:
        key_index: int. Which line index to use as the folds' comparison key.
    """
    buffer_copy = vim.current.buffer[:]
    with cursor.CursorRestorer():
        initial_folds = [vim_fold.VimFold(*f) for f in cursor.walk_over_folds()]
    sorted_folds = sorted(initial_folds, key=lambda f: f.get(key_index).lower())
    safe_folds_to_swap = reversed(list(zip(initial_folds, sorted_folds)))
    for old_fold, new_fold in safe_folds_to_swap:
        old_fold[vim.current.buffer] = new_fold[buffer_copy]
    present_result()


def present_result():
    """Modifies vim's fold level to show the sorting results."""
    with cursor.CursorRestorer():
        cursor.perform_motion('zXzC')
        level = cursor.get_fold_level()
        if level:
            vim.command(f'normal! {level}zo')
