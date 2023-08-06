clog
====

**Pretty-print things with color.**

This utility allows you to wrap `pprint` with colors.


## Usage

Pass any data into clog and it'll get pretty-printed.

    >>> from clog import clog
    >>> data = {'here': 'is some data'}
    >>> clog(data)

You can also give it a title:

    >>> clog(data, title="My Data")

Or change the color:

    >>> clog(data, title="My Data", color="red")


## Colors

This library uses the ANSI color codes from [fabric](http://www.fabfile.org/),
and it supports the following color strings:

- blue
- cyan
- green
- magenta
- red
- white
- yellow
