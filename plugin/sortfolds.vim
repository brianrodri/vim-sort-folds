" vim-sort-folds - Sort vim folds based on their first line.
" Maintainer:   Brian Rodriguez <brian@brianrodri.com>
" Version:      0.3.1
" License:      MIT license
let s:save_cpo = &cpo
set cpo&vim

function! s:RestoreCpo()
  let &cpo = s:save_cpo
  unlet s:save_cpo
endfunction

if !exists('g:loaded_sortfolds')
  call s:RestoreCpo()
  finish
endif

let g:loaded_sortfolds = 1

if !has('python3')
  echohl WarningMsg
  echom 'vim-sort-folds requires +python3.'
  finish
endif

vnoremap <silent> <Plug>SortFolds :call sortfolds#SortFolds()<CR>

call s:RestoreCpo()
