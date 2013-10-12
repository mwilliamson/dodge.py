#!/usr/bin/env python

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='dodge',
    version='0.1.4',
    description='Create data objects that can be easily converted to and from dicts suitable for use as JSON',
    long_description=read("README"),
    author='Michael Williamson',
    author_email='mike@zwobble.org',
    url='http://github.com/mwilliamson/dodge.py',
    keywords="data object serialise serialisation json",
    packages=['dodge'],
)
