#!/usr/bin/env python3
# encoding: utf-8
"""Defines utility class for working with vim folds."""
from collections import abc
import vim  # pylint: disable=import-error


class VimFold(abc.MutableSequence):  # pylint: disable=too-many-ancestors
    """Provides a mutable sequence interface for working with vim folds.

    Folds behave like a list-slice taken from vim's current buffer. Actions
    performed on them will act directly on the buffer. For example:

        >>> fold = VimFold(start_line_num=2, end_line_num=5)
        >>> fold.insert(0, 'asdf')
        # 'asdf' is now the second line in vim's current buffer. All subsequent
        # elements have been pushed by one.
        >>> fold[0]
        'asdf'

    Folds can also be indexed with a sequence. This allows the fold to behave
    like a list-slice of *that* sequence instead. For example:

        >>> fold = VimFold(start_line_num=1, end_line_num=3)
        >>> sequence = ['line 1', 'line 2', 'line 3']
        >>> fold[sequence]
        ['line 1', 'line 2']
        >>> fold[sequence] = ['line A', 'line B', 'line C']
        >>> sequence
        ['line A', 'line B', 'line C', 'line 3']
        >>> del fold[sequence]
        >>> sequence
        ['line C', 'line 2', 'line 3']

    Otherwise, folds behave like a slice of vim's current buffer.
    """
    def __init__(self, start_line_num, end_line_num):
        """Initializes a new VimFold from the given pair of line numbers.

        Args:
            start_line_num: int. Line number at which self starts (inclusive).
            end_line_num: int. Line number at which self ends (exclusive).
        """
        self._start = start_line_num - 1
        self._stop = end_line_num - 1

    def insert(self, index, value):
        """Insert value in vim's current buffer at index, starting at the fold.

        Args:
            index: int.
            value: str.
        """
        vim.current.buffer.insert(self._start + index, value)

    def __len__(self):
        """Returns the number of lines which self spans."""
        return self._stop - self._start

    def _shift_slice(self, slc):
        """Returns a copy of the given slice shifted by self's position."""
        return slice(self._start + slc.start, self._start + slc.stop, slc.step)

    def __getitem__(self, key):
        if isinstance(key, int):
            return vim.current.buffer[key]
        if isinstance(key, slice):
            return vim.current.buffer[self._shift_slice(key)]
        if isinstance(key, abc.Sequence):
            return key[self._start:self._stop]
        raise TypeError

    def __setitem__(self, key, value):
        if isinstance(key, int):
            vim.current.buffer[key] = value
        elif isinstance(key, slice):
            vim.current.buffer[self._shift_slice(key)] = value
        elif isinstance(self, abc.MutableSequence):
            key[self._start:self._stop] = value
        raise TypeError

    def __delitem__(self, key):
        if isinstance(key, int):
            del vim.current.buffer[key]
        elif isinstance(key, slice):
            del vim.current.buffer[self._shift_slice(key)]
        elif isinstance(self, abc.MutableSequence):
            del key[self._start:self._stop]
        raise TypeError
