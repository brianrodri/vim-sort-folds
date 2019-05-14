# `vim-sort-folds`

![](https://raw.github.com/obreitwi/vim-sort-folds/master/doc/demo.gif)

Sorting folds is way too tedious in vanilla vim... We're forced to:
 1. Join the lines of each individual into one
 2. Run `:sort` on them
 3. Split the lines back up

`vim-sort-folds` aims to help by introducing a function, `sortfolds#SortFolds`, to sort the folds of
a visual selection all at once.

Since folds can be created in a variety of ways, this can be especially handy for sorting arbitrary
groups of content based on their first line.


## Usage

 1. Enter visual mode
 2. Select the folds you'd like to sort
 3. `:call sortfolds#SortFolds()`

If you find yourself doing this frequently enough, you can bind it to a command and speed things up
even further!


## Installation

`vim-sort-folds` is compatible with most plugin managers. Just drop something like the following
into your `.vimrc`:
 - **[vim-plug](https://github.com/junegunn/vim-plug):** `Plug 'brianrodri/vim-sort-folds'`
 - **[Vundle](https://github.com/VundleVim/Vundle.vim):** `Plugin 'brianrodri/vim-sort-folds'`

_**NOTE:** this plugin (unapologetically) requires `+python3`._
