"""Sort vim folds based on their first line."""
from sort_folds import cursor
from sort_folds import fold
import vim  # pylint: disable=import-error

__all__ = ['sort_folds']
__version__ = '0.2.1'


def sort_folds():
    """Sorts the top-level folds intersecting vim's currently selected range."""
    with cursor.cursor_restorer():
        folds = [fold.VimFold(*line_nums) for line_nums in cursor.walk_folds()]
    if len(folds) > 1:
        sorted_folds = sorted(folds, key=lambda fold: fold[0].lower())
        fold_lines_to_reorder = []
        for old_fold, new_fold in zip(folds, sorted_folds):
            if old_fold != new_fold:
                fold_lines_to_reorder.append((old_fold, new_fold[:]))
        for old_fold, new_lines in reversed(fold_lines_to_reorder):
            vim.current.buffer[old_fold.slice] = new_lines
        present_result()


def present_result():
    """Modifies vim's fold level to present the sorted folds."""
    level = cursor.fold_level(cursor.perform_motion('zX' 'zC'))
    if level > 1:
        vim.command(f'normal! {level - 1}zo')
