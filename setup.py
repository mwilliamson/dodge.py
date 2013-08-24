#!/usr/bin/env python

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='dictobj',
    version='0.1.0',
    description='Create data objects that can be easily converted to and from dicts suitable for use as JSON',
    long_description=read("README"),
    author='Michael Williamson',
    url='http://github.com/mwilliamson/dictobj.py',
    keywords="data object serialise serialisation json",
    packages=['dictobj'],
)
