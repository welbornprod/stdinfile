# StdinFile

Reads stdin data, creates a temporary file that can be used by programs
that accept file arguments but not stdin. This program simply prints the
resulting temporary file's path, so that it can be used as an argument.

## Example
```bash
# Highlight stdinfile's source with pygments, and view in Chrome.
pygments -l python -f html -O full stdinfile.py | google-chrome "$(stdinfile)"

# Compare the difference between shfmt's output and the original using meld.
shfmt myscript.sh | meld "$(stdinfile)" myscript.sh

# Save a temporary file's path, for use later.
myfile="$(ls | stdinfile)"
echo "$myfile"
# Output: /tmp/stdinfile.kawk3fe1.tmp
cat "$myfile"
# Output: <whatever ls printed>
```

## Command Help
```
Usage:
    stdinfile [-h | -v]

Options:
    -h,--help     : Show this help message.
    -v,--version  : Show version.
```

## Dependencies

This script requires the [`docopt`](http://docopt.org) library.
It is installable with `pip`:

```
pip install docopt
```

## Installation

Clone this repo and symlink this script somewhere in `$PATH`:
```bash
git clone https://github.com/welbornprod/stdinfile.git
cd stdinfile
# Assuming ~/.local/bin is in your $PATH:
ln -s "$PWD/stdinfile.py" ~/.local/bin/stdinfile
```
