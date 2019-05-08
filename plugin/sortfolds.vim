" vim-sort-folds - Sort vim folds based on their first line.
" Maintainer:   Brian Rodriguez
" Version:      0.3.0
" License:      MIT license

" Vim plugin boilerplate.
let s:save_cpo = &cpo
set cpo&vim

if !exists('g:sortfolds_autoloaded')
  let g:sortfolds_autoloaded = 1

  if !has('python3')
    echohl WarningMsg
    echom 'vim-sort-folds requires +python3.'
    finish
  endif

  vnoremap <silent> <Plug>SortFolds :call sortfolds#SortFolds()<CR>

endif

" Vim plugin boilerplate.
let &cpo = s:save_cpo
unlet s:save_cpo
