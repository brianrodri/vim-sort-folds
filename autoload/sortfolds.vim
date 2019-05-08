" vim-sort-folds - Sort vim folds based on their first line.
" Maintainer:   Brian Rodriguez <brian@brianrodri.com>
" Version:      0.3.1
" License:      MIT license

" What can I say? I love Python :)
py3 import vim
py3 import sort_folds

function! sortfolds#SortFolds(...) range
  silent execute a:firstline . ',' . a:lastline .
      \ ' py3 sort_folds.sort_folds(' . get(a:, 0, 0) . ')'
endfunction
