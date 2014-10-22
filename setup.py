#!/usr/bin/env python

import os
from setuptools import setup
import sys

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

if sys.version_info[:2] < (2, 7):
    install_requires = ["ordereddict>=1.1,<2.0"]
else:
    install_requires = []
    
setup(
    name='dodge',
    version='0.1.6',
    description='Create data objects that can be easily converted to and from dicts suitable for use as JSON',
    long_description=read("README.rst"),
    author='Michael Williamson',
    author_email='mike@zwobble.org',
    url='http://github.com/mwilliamson/dodge.py',
    keywords="data object serialise serialisation json",
    packages=['dodge'],
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Operating System :: OS Independent',
    ],
)
