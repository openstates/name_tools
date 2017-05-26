==========
name_tools
==========

**This library is no longer maintained.**

Consider a library like `probablepeople <https://github.com/datamade/probablepeople>`_.

A Python library for manipulating and comparing English, Western-style personal names.

Released under a BSD-style license.

Source: http://github.com/openstates/name_tools

Installation
============

To install from PyPI run

   ``pip install name_tools``

or

   ``easy_install name_tools``

To install from a source package run

   ``python setup.py install``

Usage
=====

`name_tools.split(name)` breaks a name into 4 (possibly empty) parts,
representing prefixes ('Mr.', 'Dr.', etc.), a 'first part' (given names,
middle names, middle initials), a last name, and suffixes ('Jr.',
'III', 'Ph.D', etc.)

  >>> import name_tools
  >>> name_tools.split("President Barack Hussein Obama II")
  ('President', 'Barack Hussein', 'Obama', 'II')
  >>> name_tools.split("Obama, President Barack H., II")
  ('President', 'Barack H', 'Obama', 'II')
  >>> name_tools.split("Fleet Admiral William Frederick Halsey, Jr., USN")
  ('Fleet Admiral', 'William Frederick', 'Halsey', 'Jr., USN')
  >>> name_tools.split("Dick van Dyke")
  ('', 'Dick', 'van Dyke', '')

`name_tools.canonicalize(name)` returns a name in a canonical format:
'Prefixes First Last, Suffixes', with extra spaces removed and words
capitalized.

  >>> name_tools.canonicalize('  WASHBURNE,  zoe alleyne')
  'Zoe Alleyne Washburne'
  >>> name_tools.canonicalize('DR. simon tam')
  'Dr. Simon Tam'
  >>> name_tools.canonicalize(' thurston b. howell iii')
  'Thurston B. Howell, III'
  
`name_tools.match(name1, name2)` provides a measure of the
similarity between two name, considering factors such as differing word
order ('Bond, James' and 'James Bond'), use of initials
('J. R. R. Tolkien' and 'John Ronald Reuel Tolkien') and various
titles and honorifics ('Fleet Admiral William Frederick Halsey, Jr., USN',
and 'William Frederick Halsey').

  >>> name_tools.match('Eric Schmidt', 'Eric Schmidt')
  1.0
  >>> name_tools.match('Bob Dole', 'Dole, Bob')
  0.98
  >>> name_tools.match("michaeL StepHens", "MichaEl  StePhens")
  0.98
  >>> name_tools.match("Mr. X", "X")
  0.95
  >>> name_tools.match('Jeff Tweedy', 'J Tweedy')
  0.9
  >>> name_tools.match('Ferris Bueller', 'Bueller')
  0.8
  >>> name_tools.match('John Smith', 'John Johnson')
  0.0
