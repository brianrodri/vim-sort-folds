# vim-sort-folds

## Overview

![](https://raw.github.com/obreitwi/vim-sort-folds/master/doc/demo.gif)

Sorting folds is tedious in vanilla vim. You must join all lines of a fold, sort the joined lines, then split them back up. This is much more involved than most other things that vim allows you to do...

Enter: `vim-sort-folds`! It aims to solve this issue by introducing a command to sort the folds in a visually selected region. Since folds can be created in a variety of ways, it is especially handy for sorting arbitrary groups of text based on their first line.

NOTE: this plugin (unapologetically) requires `+python3`.


## Installation

`vim-sort-folds` is compatible with most of the commonly used plugin managers for vim. Just drop
something like the following lines somewhere in your `.vimrc`:

 - `Plug 'brianrodri/vim-sort-folds'` (for [vim-plug](https://github.com/junegunn/vim-plug))
 - `Plugin 'brianrodri/vim-sort-folds'` (for [Vundle](https://github.com/VundleVim/Vundle.vim))


## Note: manual foldmethod
This plugin is untested, and is not expected to work when `foldmethod` is set to `manual` (for now).
