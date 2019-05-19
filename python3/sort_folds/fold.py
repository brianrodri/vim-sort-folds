"""Utility module to make working with vim folds more pythonic."""
import collections
import vim  # pylint: disable=import-error


class VimFold(collections.abc.Sequence):
    """Interface for working with vim folds as if they were a sequence.

    VimFold behaves like a slice of vim's current buffer. No slicing actually
    occurs, however, until explicitly requested by index operations.

    All actions performed on folds reference the corresponding range in the
    buffer directly, while letting users interface through 0-based indices.

    IMPORTANT: VimFold makes no effort to keep track of any changes to vim's
    current buffer.

    Example:
        >>> vim.current.buffer = ['A', '# {{{', 'B', '# }}}', 'C']
        >>> fold = VimFold(start=1, stop=4)  # NOTE: No slices are created.
        >>> fold[1]
        'B'
        >>> fold[:]  # NOTE: Creates an actual slice.
        ['# {{{', 'B', '# }}}']
    """

    def __init__(self, start, stop):
        """Initializes a new instance from the given pair of indices.

        Args:
            start: int. Inclusive index into vim's current buffer at which a vim
                fold starts.
            stop: int. Exclusive index into vim's current buffer at which a vim
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

    @property
    def slice(self):
        """Returns the slice into vim's current buffer which self spans over."""
        return slice(self._start, self._stop, 1)

    def __repr__(self):
        class_qual_name = self.__class__.__qualname__
        return f'{class_qual_name}(start={self._start}, stop={self._stop})'

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

    def _abs_key(self, key):
        """Returns absolute value of the fold-relative key.

        Args:
            key: *.

        Returns:
            *. A corresponding key into vim's current buffer.
        """
        if isinstance(key, int):
            key = self._abs_index(key)
        elif isinstance(key, slice):
            key = self._abs_slice(key)
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
        abs_pos = max(0, pos + len(self)) if pos < 0 else min(pos, len(self))
        return self._start + abs_pos
