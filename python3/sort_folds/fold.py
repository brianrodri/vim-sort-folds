#!/usr/bin/env python3
"""Defines utility class for working with vim folds."""
import vim  # pylint: disable=import-error


class VimFold():
    """Interface for working with vim folds as if they were a mutable sequence.

    Folds behave like a list-slice taken from vim's current buffer. No slicing
    actually happens, however, because they only hold indices into the buffer.
    Regardless, actions performed on folds modify the buffer directly.

    Example:
        >>> fold = VimFold(start_line_num=2, stop_line_num=5)
        >>> fold.insert(0, 'asdf')
        # 'asdf' is now the second line in vim's current buffer. All subsequent
        # lines have been pushed by one.
        >>> fold[1]
        'asdf'

    Folds can also be indexed with a sequence. This allows the fold to behave
    like a list-slice of *that* sequence instead.

    Example:
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
        """Initializes a new instance from the given pair of line numbers.

        Args:
            start_line_num: int. Line number at which self starts (inclusive).
            stop_line_num: int. Line number at which self stops (exclusive).
        """
        self._start = start_line_num - 1
        self._stop = stop_line_num - 1

    def insert(self, index, value):
        """Insert value into vim's current buffer, offset by self and the index.

        Args:
            index: int.
            value: str.
        """
        vim.current.buffer.insert(self._start + index, value)

    def _shifted(self, aslice):
        """Returns a copy of the given slice, but shifted by self's position."""
        shift = self._start
        return slice(aslice.start + shift, aslice.stop + shift, aslice.step)

    def __len__(self):
        return self._stop - self._start

    def __iter__(self):
        return (vim.current.buffer[i] for i in range(self._start, self._stop))

    def __getitem__(self, key):
        if isinstance(key, int):
            return vim.current.buffer[self._start + key]
        if isinstance(key, slice):
            return vim.current.buffer[self._shifted(key)]
        return key[self._start:self._stop]

    def __setitem__(self, key, value):
        if isinstance(key, int):
            vim.current.buffer[self._start + key] = value
        elif isinstance(key, slice):
            vim.current.buffer[self._shifted(key)] = value
        else:
            key[self._start:self._stop] = value

    def __delitem__(self, key):
        if isinstance(key, int):
            del vim.current.buffer[self._start + key]
        elif isinstance(key, slice):
            del vim.current.buffer[self._shifted(key)]
        else:
            del key[self._start:self._stop]
