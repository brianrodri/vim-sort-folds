#!/usr/bin/env python3
# encoding: utf-8
"""Defines VimFold class to help working with folds in vim."""
import collections
import vim


class VimFold(collections.abc.MutableSequence):
    """Provides an interface for working with vim folds.

    Folds behave like slices when subscripted with a sequence:
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

    The rest of VimFold's interface acts like a sublist in vim's current buffer.
    """
    def __init__(self, start_line_num, end_line_num):
        """Initializes a new VimFold from the given pair of line numbers.

        Args:
            start_line_num: int. Line number at which self starts (inclusive).
            end_line_num: int. Line number at which self ends (exclusive).
        """
        self._start = start_line_num - 1
        self._end = end_line_num - 1

    def get(self, index):
        """Get line from vim's current buffer at index, offset by self's start.

        Args:
            index: int.

        Returns:
            str. The corresponding line in vim's current buffer, offset by
                self's position.
        """
        return vim.current.buffer[self._start + index]

    def insert(self, index, line):
        """Insert line to vim's current buffer at index, offset by self's start.

        Args:
            index: int.
            line: str.
        """
        vim.current.buffer.insert(self._start + pos, item)

    def __len__(self):
        """Returns the number of lines which self spans."""
        return self._end - self._start

    def __iter__(self):
        """Iterates through the lines of self's fold in vim's current buffer."""
        return (self._get(i) for i in range(self._start, self._end))

    def __getitem__(self, sequence):
        return sequence[self._start:self._end]

    def __setitem__(self, mutable_sequence, item):
        mutable_sequence[self._start:self._end] = item

    def __delitem__(self, mutable_sequence):
        del mutable_sequence[self._start:self._end]
