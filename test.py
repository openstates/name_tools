#!/usr/bin/env python


if __name__ == '__main__':
    import doctest
    import name_tools
    doctest.testfile('README.rst')
    doctest.testmod(name_tools)
