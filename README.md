# `vim-sort-folds`

![](https://raw.github.com/obreitwi/vim-sort-folds/master/doc/demo.gif)

Sorting folds is way too tedious in vanilla vim... we're forced to:
 1. Join the lines of each fold
 2. Sort the joined lines
 3. Split the lines back up

`vim-sort-folds` aims to help by introducing a function, `sortfolds#SortFolds`, to sort the folds of a visual selection.

Since folds can be created in a variety of ways, this can be especially handy for sorting arbitrary groups of content based on their first line.


## Usage

 1. Enter visual mode
 2. Select the folds you want sorted
 3. Call `sortfolds#SortFolds`
 
If you find yourself doing this frequently enough, you can even bind it to a command to speed things up even further!


## Installation

`vim-sort-folds` is compatible with most of the commonly used plugin managers for vim. Just drop something like the following lines somewhere in your `.vimrc`:

 - `Plug 'brianrodri/vim-sort-folds'` (for [vim-plug](https://github.com/junegunn/vim-plug))
 - `Plugin 'brianrodri/vim-sort-folds'` (for [Vundle](https://github.com/VundleVim/Vundle.vim))

_**NOTE**: this plugin (unapologetically) requires `+python3`._
