" sort-folds.vim - Sort closed folds based on first line.
" Maintainer:   Brian Rodriguez
" Version:      0.3.0
" License:      MIT license

if exists('g:sort_folds_has_finished_loading')
  finish
endif

let s:save_cpo = &cpo
set cpo&vim

if !has('python3')
  echohl WarningMsg
  echom 'sort-folds requires +python3.'
  finish
endif

let g:sort_folds_has_finished_loading = 1
let &cpo = s:save_cpo
unlet s:save_cpo
