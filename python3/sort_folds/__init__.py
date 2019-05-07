#!/usr/bin/env python3
# encoding: utf-8
"""Sort folds based on their first line.

Maintainer:	Brian Rodriguez
"""
import contextlib
import vim

__all__ = ['sort_folds']
__version__ = '0.3.0'


class Fold():
    """Iterable interface for foldable lines in vim's current buffer.

    Attributes:
        start: int. The buffer index at which the fold starts (inclusive).
        end: int. The buffer index at which the fold ends (exclusive).
    """
    def __init__(self, start_line_num, end_line_num):
        """Initializes a new Fold from the given pair of line numbers.

        Args:
            start_line_num: int. Line number at which self starts (inclusive).
            end_line_num: int. Line number at which self ends (exclusive).

        Raises:
            IndexError: The line number pair do not form a valid bound.
        """
        if start_line_num > end_line_num:
            raise IndexError(
                f'Lower bound: {start_line_num}, Upper bound: {end_line_num}')
        self.start = start_line_num - 1
        self.end = end_line_num - 1

    def __len__(self):
        return self.end - self.start

    def __getitem__(self, i):
        self_len = len(self)
        if 0 <= i < self_len:
            return vim.current.buffer[self.start + i]
        raise IndexError(f'Lower bound: 0, Upper bound: {self_len}, Index: {i}')


def sort_folds(key_index=0):
    """Sorts folds enclosed in vim's current range.

    Args:
        key_index: int. The index of the line to use as a fold's comparison key.
    """
    initial_buffer, current_buffer = vim.current.buffer[:], vim.current.buffer

    with cursor_restorer():
        initial_folds = tuple(Fold(*r) for r in walk_folds())
    sorted_folds = sorted(initial_folds, key=lambda f: f[key_index].lower())
    for dst, src in reversed(tuple(zip(initial_folds, sorted_folds))):
        current_buffer[dst.start:dst.end] = initial_buffer[src.start:src.end]
    present_result()


@contextlib.contextmanager
def cursor_restorer():
    """Context manager to restore the  cursor's position after exiting."""
    initial_cursor = vim.current.window.cursor
    try:
        yield
    finally:
        vim.current.window.cursor = initial_cursor


def walk_folds():
    """Yields the fold ranges found within the current range through motions.

    Yields:
        tuple(int, int). The starting (inclusive) and ending (exclusive) line
            numbers of a fold.
    """
    cursor = move_to_first_fold()
    at_end_of_folds = (cursor == None)
    while not at_end_of_folds and cursor < vim.current.range.end:
        start, end = (cursor, perform_motion('zo]z') + 1)
        cursor = perform_motion('zj')
        at_end_of_folds = (
            cursor == start or get_fold_level(cursor) != get_fold_level(start))
        yield (start, end)


def move_to_first_fold():
    """Places the cursor at the first fold within the current range.

    Returns:
        int or None. Line number of the first fold or None if no folds exist.
    """
    cursor = perform_motion(None)
    if not get_fold_level(cursor):
        next_fold_start = perform_motion('zj')
        if cursor == next_fold_start:
            return None
        cursor = next_fold_start
    else:
        with cursor_restorer():
            outer_fold_start = perform_motion('zo[z')
        if get_fold_level(cursor) == get_fold_level(outer_fold_start):
            cursor = outer_fold_start
    return cursor if cursor in vim.current.range else None


def present_result():
    """Modifies fold levels to show the caller their sorted results."""
    vim.command('normal! zXzC')
    level = get_fold_level(perform_motion(None))
    if level:
        vim.command(f'normal! {level}zo')


def perform_motion(motion):
    """Applies the given motion to the cursor.

    Args:
        motion: str or None. The motion to perform.

    Returns:
        int. The line number the cursor ends up on.
    """
    if motion is not None:
        vim.command(f'normal! {motion}')
    return int(vim.eval('line(".")'))


def get_fold_level(line_num):
    """Returns the fold level of the given line number.

    Args:
        line_num: int.

    Returns:
        int. The fold-level of the given line number.
    """
    return int(vim.eval(f'foldlevel({line_num})'))
