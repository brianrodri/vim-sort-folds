"""Utility class for working with vim folds."""
import enum
import vim  # pylint: disable=import-error


class _Bounds(enum.Enum):
    """Describes which range of values into a fold's elements are valid.

    Used by Fold to help emulate "real" lists.
    """
    INDICES = enum.auto()  # Requires: 0 <= value < len(fold)
    SIZES = enum.auto()  # Requires: 0 <= value <= len(fold)
    UNBOUNDED = enum.auto()  # No requirements.

    def validate(self, fold, value):
        """Returns whether the given value is within the bounds of the fold."""
        if self is INDICES:
            return -len(fold) <= value < len(fold)
        if self is SIZES:
            return -len(fold) <= value <= len(fold)
        if self is UNBOUNDED:
            return True


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

    Folds can also be indexed with a sequence, which makes a real slice of that
    sequence using the fold's positioning.

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
        ['line C', 'line 3']
    """

    def __init__(self, start, stop):
        """Initializes a new instance from the given pair of line numbers.

        Args:
            start: int. Line number at which self starts (inclusive).
            stop: int. Line number at which self stops (exclusive).

        Raises:
            ValueError: Got an invalid bound (start > stop).
        """
        if start > stop:
            raise ValueError(f'want: start <= stop, got: {start} > {stop}')
        self._start = start - 1
        self._stop = stop - 1

    def insert(self, index, value):
        """Inserts value into vim's current buffer at the index offset by self.

        Args:
            index: int.
            value: str.
        """
        vim.current.buffer.insert(self._clamp(index, _Bounds.SIZES), value)

    def __iter__(self):
        return (vim.current.buffer[i] for i in range(self._start, self._stop))

    def __len__(self):
        return self._stop - self._start

    def __getitem__(self, key):
        if isinstance(key, int):
            return vim.current.buffer[self._clamp(key, _Bounds.INDICES)]
        if isinstance(key, slice):
            return vim.current.buffer[self._shifted(key)]
        return key[self._start:self._stop]

    def __setitem__(self, key, value):
        if isinstance(key, int):
            vim.current.buffer[self._clamp(key, _Bounds.INDICES)] = value
        elif isinstance(key, slice):
            vim.current.buffer[self._shifted(key)] = value
        else:
            key[self._start:self._stop] = value

    def __delitem__(self, key):
        if isinstance(key, int):
            del vim.current.buffer[self._clamp(key, _Bounds.INDICES)]
        elif isinstance(key, slice):
            del vim.current.buffer[self._shifted(key)]
        else:
            del key[self._start:self._stop]

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

    def _clamp(self, index, bounds=_Bounds.UNBOUNDED):
        """Calculates corresponding index into fold from given 0-based index.

        Args:
            index: int. 0-based index into the fold's elements.
            strict: bool. Whether to raise an error when index is out of range.

        Returns:
            int. An index i such that: self._start <= i <= self._stop.
            bounds: _Bounds. How to determine whether the index is out of range.

        Raises:
            IndexError: When the index is out of bounds.
        """
        if not bounds.validate(self, index):
            raise IndexError('list index out of bounds')
        clamped_index = min(max(index, -len(self)), len(self)) % (len(self) + 1)
        return self._start + clamped_index
