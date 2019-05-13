# `vim-sort-folds`

## Overview

![](https://raw.github.com/obreitwi/vim-sort-folds/master/doc/demo.gif)

Sorting folds is way too tedious in vanilla vim; it requires us to:
 1. Join the lines of each fold
 2. Sort the joined lines
 3. Split the lines back up

`vim-sort-folds` aims to simplify the task by introducing a command to sort the folds of a visually selected region.

Since folds can be created in a variety of ways, this can be especially handy for sorting arbitrary groups of content based on their first line.


## Installation

`vim-sort-folds` is compatible with most of the commonly used plugin managers for vim. Just drop something like the following lines somewhere in your `.vimrc`:

 - `Plug 'brianrodri/vim-sort-folds'` (for [vim-plug](https://github.com/junegunn/vim-plug))
 - `Plugin 'brianrodri/vim-sort-folds'` (for [Vundle](https://github.com/VundleVim/Vundle.vim))

_**NOTE**: this plugin (unapologetically) requires `+python3`._
