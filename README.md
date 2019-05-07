# vim-sort-folds

## Overview

![](https://raw.github.com/obreitwi/vim-sort-folds/master/doc/demo.gif)

Sorting folds is tedious in vanilla vim. You would need to join all lines of a fold, sort the joined
lines, then split them back up. Much more involved than most other things vim allows you to do,
especially with motions.

This plugin aims to solves that issue: it provides a command to sort the folds of a visually
selected region, while keeping them in tact. Since folds can be created in a variety of ways, it is
especially handy for sorting arbitrary groups of text based on their first line.

One use-case (demonstrated above, and the motivation of the original author of this plugin) is to
sort functions alphabetically after the fact.


## Installation

`vim-sort-folds` is compatible with most of the commonly used plugin managers for vim. Just drop
something like the following lines somewhere in your `.vimrc`:

 - `Plug 'brianrodri/vim-sort-folds'` (for [vim-plug](https://github.com/junegunn/vim-plug))
 - `Plugin 'brianrodri/vim-sort-folds'` (for [Vundle](https://github.com/VundleVim/Vundle.vim))


## Note: manual foldmethod
This plugin is untested, and is not expected to work when `foldmethod` is set to `manual` (for now).
