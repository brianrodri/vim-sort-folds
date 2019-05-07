#!/usr/bin/env python3
# encoding: utf-8
"""Sort vim folds based on their first lines."""
import vim

from sort_folds import cursor
from sort_folds import fold

__all__ = ['sort_folds']
__version__ = '0.3.0'


def sort_folds(key_line_index=0):
    """Sorts the folds intersecting vim's current range.

    Args:
        key_line_index: int. The line index to use as the folds' comparison key.
    """
    with cursor.CursorRestorer():
        initial_folds = [fold.VimFold(*rng) for rng in cursor.walk_over_folds()]
    if len(initial_folds) < 2:
        return
    sorted_folds = sorted(initial_folds, key=make_fold_key(key_line_index))

    initial_buffer = vim.current.buffer[:]
    safe_folds_to_swap = reversed(list(zip(initial_folds, sorted_folds)))
    for old_fold, new_fold in safe_folds_to_swap:
        old_fold[vim.current.buffer] = new_fold[initial_buffer]
    present_result()


def make_fold_key(key_line_index):
    """Returns a function which will create keys for comparing VimFolds.

    Args:
        key_line_index: int. The line index to use as the folds' comparison key.

    Returns:
        callable(VimFold) -> Comparable.
    """
    def fold_key(fold):
        """Returns a key for comparing VimFold objects during sort.

        Args:
            fold: VimFold.

        Returns:
            Comparable.
        """
        return fold.get(key_line_index).lower()
    return fold_key


def present_result():
    """Modifies vim's fold level to show the sorting results."""
    level = cursor.get_fold_level(cursor.perform_motion('zXzC')) - 1
    if level > 0:
        vim.command(f'normal! {level}zo')
