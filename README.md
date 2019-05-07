# vim-sort-folds

## Overview

![](https://raw.github.com/obreitwi/vim-sort-folds/master/doc/demo.gif)

Sorting folds is not easily possible in vanilla vim. You could join all lines in a fold, sort, then
split them up again; but that is time consuming and tedious.

This little plugin solves that issue: it sorts a visually selected region while keeping closed folds
intact. Since folds can be created in a variety of ways, it is therefore straight-forward to sort
arbitrary groups of text based on their first line.

One use-case (demonstrated above and the original motivation for this plugin) is to sort functions
alphabetically after the fact.


## Installation

`vim-sort-folds` is compatible to the most commonly used plugin managers for vim. Just drop the
following line in your `.vimrc`:

`Plug 'brianrodri/vim-sort-folds'` (for [vim-plug](https://github.com/junegunn/vim-plug))

`Plugin 'brianrodri/vim-sort-folds'`
(for [Vundle](https://github.com/VundleVim/Vundle.vim))


## Note: manual foldmethod
This plugin is untested, and is not expected to work when `foldmethod` is set to `manual` (for now).
