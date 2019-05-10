"""Utility class for working with vim folds."""
import collections
import vim  # pylint: disable=import-error


class VimFold(collections.abc.MutableSequence):  # pylint: disable=too-many-ancestors
    """Interface for working with vim folds as if they were a mutable sequence.

    Folds behave like a slice of vim's current buffer. No slicing actually
    occurs, however, as they only hold indices into the buffer. Regardless,
    actions performed on folds modify the buffer directly.

    Example:
        >>> fold = VimFold(start_line_num=2, stop_line_num=5)
        >>> fold.insert(0, 'something')
        # 'something' is now the second line in vim's current buffer. All
        # subsequent lines have been pushed by one.
        >>> fold[1]
        'something'
    """

    def __init__(self, start, stop):
        """Initializes a new instance from the given pair of line numbers.

        Args:
            start: int. Line number at which self starts (inclusive).
            stop: int. Line number at which self stops (exclusive).

        Raises:
            IndexError: range is invalid.
        """
        if start > stop:
            raise IndexError(f'range is invalid: start={start} > stop={stop}')
        self._start = start - 1
        self._stop = stop - 1

    @property
    def start(self):
        """Read-only access to start index of self."""
        return self._start

    @property
    def stop(self):
        """Read-only access to stop index of self."""
        return self._stop

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            f'start={self._start}, stop={self._stop}, '
            f'lines_view=[{", ".join(self)}])')

    __hash__ = None

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return (self._start, self._stop) == (other.start, other.stop)
        return NotImplemented

    def __len__(self):
        return self._stop - self._start

    def __iter__(self):
        return (vim.current.buffer[i] for i in range(self._start, self._stop))

    def __getitem__(self, key):
        if isinstance(key, int):
            return vim.current.buffer[self._clamp(key, strict=True)]
        if isinstance(key, slice):
            return vim.current.buffer[self._shifted(key)]
        raise IndexError(f'invalid index: {key!r}')

    def __setitem__(self, key, value):
        if isinstance(key, int):
            vim.current.buffer[self._clamp(key, strict=True)] = value
        elif isinstance(key, slice):
            vim.current.buffer[self._shifted(key)] = value
        else:
            raise IndexError(f'invalid index: {key!r}')

    def __delitem__(self, key):
        if isinstance(key, int):
            del vim.current.buffer[self._clamp(key, strict=True)]
        elif isinstance(key, slice):
            del vim.current.buffer[self._shifted(key)]
        else:
            raise IndexError(f'invalid index: {key!r}')

    def insert(self, index, value):
        """Inserts value into vim's current buffer at the index offset by self.

        Args:
            index: int.
            value: str.
        """
        vim.current.buffer.insert(self._clamp(index), value)

    def _shifted(self, aslice):
        """Returns a copy of the given slice, but shifted by self's position.

        Args:
            aslice: slice.

        Returns:
            slice.
        """
        return slice(
            self._start if aslice.start is None else self._clamp(aslice.start),
            self._stop if aslice.stop is None else self._clamp(aslice.stop),
            aslice.step)

    def _clamp(self, index, strict=False):
        """Calculates the range-respecting value of the given 0-based index.

        Args:
            index: int. 0-based index into the fold's slice. Negative values are
                allowed, and behave as they would for lists.
            strict: bool. Whether to raise an error when the index is out of
                the fold's range.

        Returns:
            int. An index, i, such that: self.start <= i <= self.stop.

        Raises:
            IndexError: when called with an out-of-range index in strict mode.
        """
        self_len = len(self)
        if strict and not -self_len <= index < self_len:
            raise IndexError('list index out of range')
        clamped_index = (
            max(index + self_len, 0) if index < 0 else min(index, self_len))
        return self._start + clamped_index
