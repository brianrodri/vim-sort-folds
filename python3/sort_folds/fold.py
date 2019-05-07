#!/usr/bin/env python3
# encoding: utf-8
"""Defines utility class for working with vim folds."""
import vim  # pylint: disable=import-error


class VimFold():
    """Provides a mutable sequence interface for working with vim folds.

    Folds behave like a list-slice taken from vim's current buffer, but they
    only hold indices into it. Actions performed on them will act directly on
    the buffer. For example:

        >>> fold = VimFold(start_line_num=2, stop_line_num=5)
        >>> fold.insert(0, 'asdf')
        # 'asdf' is now the second line in vim's current buffer. All subsequent
        # lines have been pushed by one.
        >>> fold[1]
        'asdf'

    Folds can also be indexed with a sequence. This allows the fold to behave
    like a list-slice of *that* sequence instead. For example:

        >>> fold = VimFold(start_line_num=1, stop_line_num=3)
        >>> sequence = ['line 1', 'line 2', 'line 3']
        >>> fold[sequence]
        ['line 1', 'line 2']
        >>> fold[sequence] = ['line A', 'line B', 'line C']
        >>> sequence
        ['line A', 'line B', 'line C', 'line 3']
        >>> del fold[sequence]
        >>> sequence
        ['line C', 'line 2', 'line 3']

    """
    def __init__(self, start_line_num, stop_line_num):
        """Initializes a new VimFold from the given pair of line numbers.

        Args:
            start_line_num: int. Line number at which self starts (inclusive).
            stop_line_num: int. Line number at which self stops (exclusive).
        """
        self._start = start_line_num - 1
        self._stop = stop_line_num - 1

    def insert(self, index, value):
        """Insert value in vim's current buffer at index, starting at the fold.

        Args:
            index: int.
            value: str.
        """
        vim.current.buffer.insert(self._start + index, value)

    def __len__(self):
        return self._stop - self._start

    def __iter__(self):
        yield from (
            vim.current.buffer[i] for i in range(self._start, self._stop))

    def _shifted(self, aslice):
        """Returns a copy of the given slice shifted by self's position."""
        shift = self._start
        return slice(aslice.start + shift, aslice.stop + shift, aslice.step)

    def __getitem__(self, key):
        if isinstance(key, int):
            return vim.current.buffer[key]
        if isinstance(key, slice):
            return vim.current.buffer[self._shifted(key)]
        # Finally, assume key to be a sequence.
        return key[self._start:self._stop]

    def __setitem__(self, key, value):
        if isinstance(key, int):
            vim.current.buffer[key] = value
        elif isinstance(key, slice):
            vim.current.buffer[self._shifted(key)] = value
        else:
            # Finally, assume key to be a mutable sequence.
            key[self._start:self._stop] = value

    def __delitem__(self, key):
        if isinstance(key, int):
            del vim.current.buffer[key]
        elif isinstance(key, slice):
            del vim.current.buffer[self._shifted(key)]
        else:
            # Finally, assume key to be a mutable sequence.
            del key[self._start:self._stop]
