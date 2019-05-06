" SortFolds.vim - Sort closed folds based on first line
" Maintainer:   Brian Rodriguez
" Version:      0.3.0
" License:      MIT license
py3 import vim
py3 import SortFolds

function! SortFolds#SortFolds(...) range
    silent execute a:firstline . ", " . a:lastline .
                \ " py3 SortFolds.sort_folds(" . get(a:, 0, 0) .  ")"
endfunction
