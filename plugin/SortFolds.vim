" SortFolds.vim - Sort closed folds based on first line
" Maintainer:   Brian Rodriguez
" Version:      0.3.0
" License:      MIT license

if exists("g:loaded_sort_folds")
    finish
endif
let g:loaded_sort_folds = 1

let s:save_cpo = &cpo
set cpo&vim

if !has("python3")
    echohl WarningMsg
    echom "SortFolds requires +python3."
    finish
endif

vnoremap <silent> <Plug>SortFolds :call SortFolds#SortFolds()<CR>

let &cpo = s:save_cpo
