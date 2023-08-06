# python-bautils

bautils is a Python module implementing some useful helper functions for
working with the Python [bitarray](https://pypi.python.org/pypi/bitarray/)
module. Specifically, bautils supports adding (and, coming soon) other
basic arithmetic operations on bitarrays as if they were arbitrary length
binary numbers, something the bitarray package itself doesn't seem to
support.

I opted to put these functions in a new module; none are terribly complicated
to implement, so they're essentially just a set of convenient wrappers.

Currently bautils just contains the following routines. More work is
planned for the future:

```add(b1, b2)```: add two bitarrays together, returns the result.

```left(ba, n)```: shifts a bitarray left by n, preserving the original size.

```right(ba, n)```: shifts a bitarray right by n, preserving the original size.

```random(length)```: returns a random bitarray of size length.

```maxb(b1, b2)```: returns the larger bitarray.

```minb(b1, b2)```: returns the smaller bitarray.

Unit tests are also a work in progress.

# Credits, Legal

bautils is written by Ben Rosser <rosser.bjr@gmail.com>, and is released
under the MIT License (see LICENSE file).
