#!/usr/bin/env python3
# encoding: utf-8
"""Sort vim folds based on their first lines."""
import collections
import contextlib
import vim

__all__ = ['sort_folds']
__version__ = '0.3.0'


class Fold(collections.abc.MutableSequence):
    """An interface for working with the foldable lines in vim's current buffer.

    Folds behave like sequences when subscripted using another sequence:
        >>> fold = Fold(start_line_num=1, end_line_num=3)
        >>> sequence = ['line 1', 'line 2', 'line 3']
        >>> fold[sequence]
        ['line 1', 'line 2']
        >>> fold[sequence] = ['line A', 'line B', 'line C']
        >>> sequence
        ['line A', 'line B', 'line C', 'line 3']
        >>> del fold[sequence]
        >>> sequence
        ['line C', 'line 2', 'line 3']

    Attributes:
        start: int. The buffer index at which the fold starts (inclusive).
        end: int. The buffer index at which the fold ends (exclusive).
    """
    def __init__(self, start_line_num, end_line_num):
        """Initializes a new Fold from the given pair of line numbers.

        Args:
            start_line_num: int. Line number at which self starts (inclusive).
            end_line_num: int. Line number at which self ends (exclusive).
        """
        self.start = start_line_num - 1
        self.end = end_line_num - 1

    def get(self, index):
        """Gets line from vim's current buffer at the given index.

        Args:
            index: int.

        Returns:
            str. The corresponding str from vim's current buffer offset by the
                fold's position.
        """
        return vim.current.buffer[self.start + i]

    def insert(self, buf, item):
        """Inserts an item before the fold's position in the given buf.

        Args:
            buf: collections.abc.MutableSequence.
            item: str.
        """
        buf.insert(self.start, item)

    def __iter__(self):
        """Iterates through self's fold in vim's current buffer."""
        return (self.get(i) for i in range(self.start, self.end))

    def __len__(self):
        return self.end - self.start

    def __getitem__(self, buf):
        return buf[self.start:self.end]

    def __setitem__(self, buf, iterable):
        buf[self.start:self.end] = iterable

    def __delitem__(self, buf):
        del buf[self.start:self.end]


def sort_folds(key_index=0):
    """Sorts the folds intersecting vim's current range.

    Args:
        key_index: int. Which line index to use as the folds' comparison key.
    """
    buffer_copy = vim.current.buffer[:]
    with cursor_restorer():
        initial_folds = [Fold(*r) for r in walk_over_folds()]
    sorted_folds = sorted(initial_folds, key=lambda f: f.get(key_index).lower())
    safe_folds_to_swap = reversed(list(zip(initial_folds, sorted_folds)))
    for old_fold, new_fold in safe_folds_to_swap:
        old_fold[vim.current.buffer] = new_fold[buffer_copy]
    present_result()


@contextlib.contextmanager
def cursor_restorer():
    """Context manager to restore vim's cursor position after exiting."""
    initial_cursor = vim.current.window.cursor
    try:
        yield
    finally:
        vim.current.window.cursor = initial_cursor


def walk_over_folds():
    """Yields ranges of foldable line numbers while moving vim's cursor.

    Yields:
        tuple(int, int). The starting (inclusive) and ending (exclusive) line
            numbers of a fold.
    """
    cursor = move_to_first_fold()
    at_end_of_folds = (cursor is None)
    while not at_end_of_folds and cursor in vim.current.range:
        start, end = (cursor, perform_motion('zo]z') + 1)
        yield (start, end)
        cursor = perform_motion('zj')
        at_end_of_folds = (
            cursor == start or get_fold_level(cursor) != get_fold_level(start))


def move_to_first_fold():
    """Places vim's cursor at the first fold intersecting vim's current range.

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
            prev_fold_start = perform_motion('zo[z')
        if get_fold_level(cursor) == get_fold_level(prev_fold_start):
            cursor = prev_fold_start
    return cursor if cursor in vim.current.range else None


def present_result():
    """Modifies vim's fold level to display the folds that have been sorted."""
    level = get_fold_level(perform_motion('zXzC'))
    if level:
        vim.command(f'normal! {level}zo')


def perform_motion(motion):
    """Moves vim's cursor according to the given motion.

    Args:
        motion: str or None. The motion to perform.

    Returns:
        int. The line number on which the cursor ends upon.
    """
    if motion is not None:
        vim.command(f'normal! {motion}')
    return int(vim.eval('line(".")'))


def get_fold_level(line_num):
    """Returns the fold level for the given line number.

    Args:
        line_num: int.

    Returns:
        int. The fold level for the given line number.
    """
    return int(vim.eval(f'foldlevel({line_num})'))
