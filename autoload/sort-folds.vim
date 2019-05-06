" sort-folds.vim - Sort closed folds based on first line.
" Maintainer:   Brian Rodriguez
" Version:      0.3.0
" License:      MIT license

py3 import vim
py3 import sort_folds

function! SortFolds#SortFolds(...) range
  silent execute a:firstline . ',' . a:lastline . ' py3 sort_folds.sort_folds('
      \ . get(a:, 0, 1) . ')'
endfunction
