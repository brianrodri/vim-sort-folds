"""Sort vim folds based on their first line."""
from sort_folds import cursor
from sort_folds import fold
import vim  # pylint: disable=import-error

__all__ = ['sort_folds']
__version__ = '0.1.0'


def sort_folds(line_index_key=0):
    """Sorts the top-level folds intersecting vim's currently selected range.

    Args:
        line_index_key: int. The index of the line to use as a folds' key.
    """
    with cursor.cursor_restorer():
        folds = [fold.VimFold(*line_nums) for line_nums in cursor.walk_folds()]
    if len(folds) > 1:
        sorted_folds = sorted(folds, key=lambda f: f[line_index_key].lower())
        fold_lines_to_reorder = []
        for old_fold, new_fold in zip(folds, sorted_folds):
            if old_fold != new_fold:
                fold_lines_to_reorder.append((old_fold, new_fold[:]))
        for old_fold, new_lines in reversed(fold_lines_to_reorder):
            old_fold[:] = new_lines
        present_result()


def present_result():
    """Modifies vim's fold level to present the sorted lines."""
    level = cursor.fold_level(cursor.perform_motion('zX' 'zC'))
    if level > 1:
        vim.command(f'normal! {level - 1}zo')
