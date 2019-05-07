#!/usr/bin/env python3
# encoding: utf-8
"""Sort vim folds based on their first lines."""
import vim

from sort_folds import cursor
from sort_folds import fold

__all__ = ['sort_folds']
__version__ = '0.3.0'


def sort_folds(key_index=0):
    """Sorts the folds intersecting vim's current range.

    Args:
        key_index: int. Which line index to use as the folds' comparison key.
    """
    with cursor.CursorRestorer():
        initial_folds = [fold.VimFold(*rng) for rng in cursor.walk_over_folds()]
    if len(initial_folds) < 2:
        return
    sorted_folds = sorted(initial_folds, key=lambda f: f.get(key_index).lower())

    initial_buffer = vim.current.buffer[:]
    safe_folds_to_swap = reversed(list(zip(initial_folds, sorted_folds)))
    for old_fold, new_fold in safe_folds_to_swap:
        old_fold[vim.current.buffer] = new_fold[initial_buffer]
    present_result()


def present_result():
    """Modifies vim's fold level to show the sorting results."""
    with cursor.CursorRestorer():
        level = cursor.get_fold_level(cursor.perform_motion('zXzC')) - 1
        if level:
            vim.command(f'normal! {level}zo')
