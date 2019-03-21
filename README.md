# tpless
*a bad `less` clone built with [termpixels][termpixels]*

![screenshot](promo.png)

## Usage
`tpless.py` accepts a file path as a command line argument, or data on stdin (though it does not yet support non-terminal stdin, e.g. a pipe). It sort of implements a few vim-like keybindings.

* `q` to quit
* arrow keys to move around
* `g` to go to the start of the file
* `G` to go to the end of the file
* `/` to type a search term
    * `enter` to search for the next occurrence
    * `n` to continue finding the next occurrence
    * The screen is scrolled to place the result on the first line

[termpixels]: https://github.com/loganzartman/termpixels