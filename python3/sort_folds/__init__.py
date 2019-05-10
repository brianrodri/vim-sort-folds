"""Sort vim folds based on their first line."""
from sort_folds import cursor
from sort_folds import fold
import vim  # pylint: disable=import-error

__all__ = ['sort_folds']
__version__ = '1.0.0'


def sort_folds(line_index_key=0):
    """Sorts consecutive, equal-level folds in vim's currently selected range.

    Args:
        line_index_key: int. Index into the folds' lines; used for comparison.
    """
    with cursor.CursorRestorer():
        folds = [fold.VimFold(*line_nums) for line_nums in cursor.walk_folds()]
    if len(folds) > 1:
        sorted_folds = sorted(folds, key=lambda f: f[line_index_key].lower())
        sorted_fold_lines = (fold[:] for fold in sorted_folds)
        safe_assignment_order = reversed(list(zip(folds, sorted_fold_lines)))
        for out_of_order_fold, in_order_fold_lines in safe_assignment_order:
            out_of_order_fold[:] = in_order_fold_lines
        present_result()


def present_result():
    """Modify vim's fold level to present the sorted lines."""
    level = cursor.fold_level(cursor.perform_motion('zXzC'))
    if level > 1:
        vim.command(f'normal! {level - 1}zo')
