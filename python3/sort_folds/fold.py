"""Utility class for working with vim folds."""
import collections
import vim  # pylint: disable=import-error


class VimFold(collections.abc.MutableSequence):  # pylint: disable=too-many-ancestors
    """Interface for working with vim folds as if they were a mutable sequence.

    VimFold behaves like a slice of vim's current buffer. No slicing actually
    occurs, however, unless explicitly requested through index operations. All
    other actions performed on folds modify the corresponding range in the
    buffer directly, while letting users interface through 0-based indices.

    For example:
        >>> fold = VimFold(start=1, stop=4)
        >>> fold.insert(0, 'something')
        >>> vim.current.buffer[1]
        'something'
    """

    def __init__(self, start, stop):
        """Initializes a new instance from the given pair of indices.

        Args:
            start: int. An (inclusive) index into vim's current buffer at which
                a fold starts.
            stop: int. An (exclusive) index into vim's current buffer at which a
                fold stops.

        Raises:
            IndexError: range is invalid.
        """
        if start > stop:
            raise IndexError(f'range is invalid: start={start} > stop={stop}')
        self._start, self._stop = start, stop

    @property
    def start(self):
        """Provides read-only access to start index."""
        return self._start

    @property
    def stop(self):
        """Provides read-only access to stop index."""
        return self._stop

    def __repr__(self):
        cls = self.__class__.__qualname__
        return f'{cls}(start={self._start}, stop={self._stop})'

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
        """Inserts value into vim's current buffer at the fold-relative index.

        Args:
            index: int.
            value: str.
        """
        vim.current.buffer.insert(self._abs(index), value)
        self._stop += 1

    def _abs_key(self, key):
        """Returns absolute value of the fold-relative key.

        Args:
            key: *.

        Returns:
            *. A corresponding key into vim's current buffer.
        """
        if isinstance(key, int):
            return self._abs_index(key)
        if isinstance(key, slice):
            return self._abs_slice(key)
        return key

    def _abs_index(self, idx):
        """Returns absolute value of the fold-relative index.

        Args:
            idx: int.

        Returns:
            int. A corresponding index into vim's current buffer.

        Raises:
            IndexError: the relative index is out of the fold's range.
        """
        if -len(self) <= idx < len(self):
            return self._abs(idx)
        raise IndexError('list index out of range')

    def _abs_slice(self, sli):
        """Returns absolute value of the fold-relative slice.

        Args:
            sli: slice.

        Returns:
            slice. A corresponding slice into vim's current buffer.
        """
        return slice(self._start if sli.start is None else self._abs(sli.start),
                     self._stop if sli.stop is None else self._abs(sli.stop),
                     sli.step)

    def _abs(self, pos):
        """Returns absolute value of the fold-relative position.

        Args:
            pos: int.

        Returns:
            int. The corresponding position in vim's current buffer.
        """
        abs_pos = max(pos + len(self), 0) if pos < 0 else min(pos, len(self))
        return self._start + abs_pos
