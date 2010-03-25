#!/usr/bin/env python
from distutils.core import setup
from name_tools import __version__

long_description = open('README.rst').read()

setup(name="name_tools",
      version=__version__,
      packages=['name_tools'],
      description="Library for manipulating and comparing (English) names",
      author="Michael Stephens",
      author_email="me@mikej.st",
      license="BSD",
      url="http://github.com/mikejs/name_tools",
      long_description=long_description,
      platforms=["any"],
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Text Processing :: Linguistic"])
