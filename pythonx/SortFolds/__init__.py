#!/usr/bin/env python3
# encoding: utf-8
"""Sort closed folds based on their first line.

Maintainer:		Brian Rodriguez
"""
import itertools
import vim

__all__ = ["debug", "print_foldlevel", "sort_folds"]
__version__ = "0.3.0"


class Fold():
    """
        Object representing a fold in the current buffer.
    """
    def __init__(self, level, start, end=None, length=None):
        """
            Describes fold of `level` at starting line `start` till line `end`
            (0-index) of length `length`.
        """
        assert end is None or length is None
        assert end is not None or length is not None

        self.level = level
        self.start = start

        if length is None:
            self.end = end
        else:
            self.end = self.start + length

    def __len__(self):
        return self.end - self.start

    def __getitem__(self, line_number):
        return vim.current.buffer[self.start + line_number]

    @property
    def lines(self):
        for line in vim.current.buffer[self.start:self.end]:
            yield line


def debug(sorting_line_number=1):
    """
        Print debug information about how folds are extracted and sorted.
    """
    print("###############")
    print("#  Extracted  #")
    print("###############")

    print_folds(get_folds())

    print("############")
    print("#  Sorted  #")
    print("############")

    sorted_folds = sorted(get_folds(), key=lambda f: f[sorting_line_number])
    print_folds(sorted_folds)


def get_foldlevel(lineno):
    "Get foldlevel for given line number in current buffer."
    return int(vim.eval(f"foldlevel({lineno})"))


def get_folds():
    """
        Map visible folds in the appropriate area [start, end].

        We step through the region until we leave it or run out of folds.
    """
    cr = vim.current.range
    # restore cursor position
    pos = vim.current.window.cursor

    # set to starting line
    fold_start = cr.start
    fold_end = -1
    # adjust for line numbers starting at one
    normal(cr.start + 1)

    def next_fold():
        "Advance to next fold and return line number."
        normal("zj")
        # adjust for line numbers starting at one
        return int(vim.eval("line('.')")) - 1

    while fold_end != cr.end:
        fold_end = min(next_fold(), cr.end)

        if fold_end < fold_start:
            # we are iterating on the last fold, which is closed, therefore we
            # seem to jump back in lines -> we are done
            break

        if fold_end == fold_start:
            # If we ran out of folds, just put everything till the end in a
            # pseudo fold
            fold_end = cr.end

        if fold_end == cr.end:
            # adjust for having reached the end
            fold_end += 1

        fold = Fold(level=get_foldlevel(fold_start),
                    start=fold_start,
                    end=fold_end)

        if len(fold) > 0:
            yield fold

        fold_start = fold_end

    # restore cursor position
    vim.current.window.cursor = pos


def line_range_to_foldlevel(start, end):
    """
        Get the fold level for all lines in [start, end] in the current buffer.

        (Unfortunately, this is not enough to find all folds, as adjacent folds
        can have the same line number).
    """
    return map(get_foldlevel, range(start, end+1))


def normal(cmd):
    "Convenience function for unremapped normal commands."
    return vim.command("normal! {}".format(cmd))


def print_foldlevel():
    """
        Print foldlevel of fall lines in current range.
    """
    cr = vim.current.range
    for lvl, line in zip(line_range_to_foldlevel(cr.start, cr.end), cr[:]):
        print(lvl, line)


def print_folds(folds):
    """
        Prints all supplied folds for debug purposes.
    """
    for fold in folds:
        print("---")
        for line in fold.lines:
            print(fold.level, line)


def sort_folds(sort_line=0):
    sorted_folds = sorted(get_folds(), key=lambda f: f[sort_line])
    sorted_lines = (
        list(itertools.chain.from_iterable(f.lines for f in sorted_folds)))
    vim.current.range[:] = sorted_lines
