" vim-sort-folds - Sort vim folds based on their first line.
" Maintainer:   Brian Rodriguez
" Version:      0.3.0
" License:      MIT license

if exists('g:sortfolds_autoloaded')
  finish
endif
let g:sortfolds_autoloaded = 1
let s:save_cpo = &cpo
set cpo&vim

if !has('python3')
  echohl WarningMsg
  echom 'vim-sort-folds requires +python3.'
  finish
endif

vnoremap <silent> <Plug>SortFolds :call sortfolds#SortFolds()<CR>

let &cpo = s:save_cpo
