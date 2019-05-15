"""Utility module to help modify the folds of vim in a Pythonic way."""
import collections
import vim  # pylint: disable=import-error


class VimFold(collections.abc.MutableSequence):  # pylint: disable=too-many-ancestors
    """Interface for working with vim folds as if they were a mutable sequence.

    VimFold behaves like a slice of vim's current buffer. No slicing actually
    occurs, however, unless slices are the expected return value.

    All actions performed on folds act directly on the corresponding range in
    vim's current buffer.

    Example:
        >>> vim.current.buffer = ['A', 'B', 'C', 'D', 'E']
        >>> fold = VimFold(start=1, stop=4)
        >>> fold[-1]
        'D'
        >>> fold.insert(0, 'Bee')
        >>> vim.current.buffer
        ['A', 'Bee', 'B', 'C', 'D', 'E']
        >>> del fold[1]
        >>> vim.current.buffer
        ['A', 'Bee', 'C', 'D', 'E']
        >>> fold[2] = 'Dee'
        >>> vim.current.buffer
        ['A', 'Bee', 'C', 'Dee', 'E']
        >>> fold[-2:]
        ['C', 'Dee']
    """

    def __init__(self, start, stop):
        """Initializes a new instance from the given pair of indices.

        Args:
            start: int. An (inclusive) index into vim's current buffer at which
                a fold starts.
            stop: int. An (exclusive) index into vim's current buffer at which a
                fold stops.

        Raises:
            IndexError: The range is invalid.
        """
        if start > stop:
            raise IndexError(f'range is invalid: start={start} > stop={stop}')
        self._start, self._stop = start, stop

    @property
    def start(self):
        """Provides read-only access to the start index."""
        return self._start

    @property
    def stop(self):
        """Provides read-only access to the stop index."""
        return self._stop

    def __repr__(self):
        pretty_class_name = self.__class__.__qualname__
        return f'{pretty_class_name}(start={self._start}, stop={self._stop})'

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
        return vim.current.buffer[self._abs_key(key)]

    def __setitem__(self, key, value):
        vim.current.buffer[self._abs_key(key)] = value

    def __delitem__(self, key):
        del vim.current.buffer[self._abs_key(key)]

    def insert(self, index, value):
        """Inserts a value into vim's current buffer at the fold-relative index.

        Args:
            index: int.
            value: *.
        """
        vim.current.buffer.insert(self._abs_position(index), value)

    def _abs_key(self, k):
        """Returns corresponding key with respect to vim's current buffer.

        Args:
            k: *. A key into the lines of self's fold.

        Returns:
            *. A corresponding key into vim's current buffer.
        """
        if isinstance(k, int):
            return self._abs_index(k)
        if isinstance(k, slice):
            return self._abs_slice(k)
        return k

    def _abs_index(self, i):
        """Returns corresponding index with respect to vim's current buffer.

        Args:
            i: int. An index into the lines of self's fold.

        Returns:
            int. A corresponding index into vim's current buffer.

        Raises:
            IndexError: The index is out of the fold's range.
        """
        if -len(self) <= i < len(self):
            return self._abs_position(i)
        raise IndexError(f'list index={i} out of range')

    def _abs_slice(self, s):
        """Returns corresponding slice with respect to vim's current buffer.

        Args:
            s: slice. A slice into the lines of self's fold.

        Returns:
            slice. A corresponding slice into vim's current buffer.
        """
        return slice(
            self._start if s.start is None else self._abs_position(s.start),
            self._stop if s.stop is None else self._abs_position(s.stop),
            s.step)

    def _abs_position(self, p):
        """Returns corresponding position with respect to vim's current buffer.

        Args:
            p: int. A position into the lines of self's fold.

        Returns:
            int. A corresponding position into vim's current buffer.
        """
        abs_position = max(0, p + len(self)) if p < 0 else min(p, len(self))
        return self._start + abs_position
