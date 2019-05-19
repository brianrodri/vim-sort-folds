" vim-sort-folds - Sort vim folds based on their first line.
" Maintainer:   Brian Rodriguez <brian@brianrodri.com>
" Version:      0.2.2
" License:      MIT license
let s:save_cpo = &cpo
set cpo&vim

function! s:RestoreCpo()
  let &cpo = s:save_cpo
  unlet s:save_cpo
endfunction

if exists('g:is_sortfolds_loaded')
  call s:RestoreCpo()
  finish
endif
let g:is_sortfolds_loaded = 1

if !has('python3')
  echohl WarningMsg
  echom 'vim-sort-folds requires +python3.'
  call s:RestoreCpo()
  finish
endif

vnoremap <silent> <Plug>SortFolds :call sortfolds#SortFolds()

call s:RestoreCpo()
