"""Utility class for working with vim folds."""
import collections
import vim  # pylint: disable=import-error


class VimFold(collections.abc.MutableSequence):  # pylint: disable=too-many-ancestors
    """Interface for working with vim folds as if they were a mutable sequence.

    Folds behave like a slice of vim's current buffer. No slicing actually
    occurs, however, unless explicitly requested by the slice operations. All
    other actions performed on folds modify the corresponding range in the
    buffer directly.

    Example:
        >>> fold = VimFold(start=1, stop=4)
        >>> fold.insert(0, 'something')
        >>> vim.current.buffer[1]
        'something'
    """

    def __init__(self, start, stop):
        """Initializes a new instance from the given pair of indices.

        Args:
            start: int. Index at which a fold starts (inclusive).
            stop: int. Index at which a fold stops (exclusive).

        Raises:
            IndexError: range is invalid.
        """
        if start > stop:
            raise IndexError(f'range is invalid: start={start} > stop={stop}')
        self._start, self._stop = start, stop

    @property
    def start(self):
        """Returns read-only access to self's start index."""
        return self._start

    @property
    def stop(self):
        """Returns read-only access to self's stop index."""
        return self._stop

    def __repr__(self):
        class_qualname = self.__class__.__qualname__
        return f'{class_qualname}(start={self._start}, stop={self._stop})'

    __hash__ = None

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return (other.start, other.stop) == (self._start, self._stop)
        return NotImplemented

    def __len__(self):
        return self._stop - self._start

    def __iter__(self):
        return (vim.current.buffer[i] for i in range(self._start, self._stop))

    def __getitem__(self, key):
        return vim.current.buffer[self._abs(key)]

    def __setitem__(self, key, value):
        vim.current.buffer[self._abs(key)] = value

    def __delitem__(self, key):
        del vim.current.buffer[self._abs(key)]

    def insert(self, index, value):
        """Inserts value into vim's current buffer at given fold-relative index.

        Args:
            index: int.
            value: str.
        """
        vim.current.buffer.insert(self._abs_position(index), value)
        self._stop += 1

    def _abs(self, key):
        """Returns corresponding absolute value of given fold-relative key.

        Args:
            key: *. The relative key of the fold.

        Returns:
            *. The corresponding absolute key of vim's current buffer.
        """
        if isinstance(key, int):
            return self._abs_index(key)
        if isinstance(key, slice):
            return self._abs_slice(key)
        return key

    def _abs_index(self, idx):
        """Returns corresponding absolute value of given fold-relative index.

        Args:
            idx: int. The relative index into the fold.

        Returns:
            int. The corresponding absolute index of vim's current buffer.

        Raises:
            IndexError: the relative index is out of the fold's range.
        """
        if not -len(self) <= idx < len(self):
            raise IndexError('list index out of range')
        return self._abs_position(idx)

    def _abs_slice(self, sli):
        """Returns corresponding absolute value of given fold-relative slice.

        Args:
            sli: slice. A relative slice into the fold.

        Returns:
            slice. The corresponding absolute slice of vim's current buffer.
        """
        return slice(
            self._start if sli.start is None else self._abs_position(sli.start),
            self._stop if sli.stop is None else self._abs_position(sli.stop),
            sli.step)

    def _abs_position(self, pos):
        """Returns corresponding absolute value of given fold-relative position.

        Args:
            pos: int. A relative position in fold.

        Returns:
            int. The corresponding absolute position of vim's current buffer.
        """
        abs_pos = max(pos + len(self), 0) if pos < 0 else min(pos, len(self))
        return self._start + abs_pos
