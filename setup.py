#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Setup script for freebible.

Latest version can be found at https://github.com/neocl/freebible

@author: Le Tuan Anh <tuananh.ke@gmail.com>
@license: MIT
'''

# Copyright (c) 2018, Le Tuan Anh <tuananh.ke@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

########################################################################

import io
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import freebible

########################################################################


here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


long_description = read('README.md', 'CHANGES.md')

setup(
    name='freebible',
    version=freebible.__version__,
    url=freebible.__url__,
    project_urls={
        "Bug Tracker": "https://github.com/neocl/freebible/issues",
        "Source Code": "https://github.com/neocl/freebible/"
    },
    keywords="free holy bible nlp",
    license=freebible.__license__,
    author=freebible.__author__,
    tests_require=['chirptext >= 0.1a6'],
    install_requires=['chirptext >= 0.1a6'],
    author_email=freebible.__email__,
    description=freebible.__description__,
    long_description=long_description,
    packages=['freebible', 'freebible.data', 'freebible.parsers'],
    package_data={'freebible': ['data/kougo/*.gz',
                                'data/web/*.gz']},
    include_package_data=True,
    platforms='any',
    test_suite='test',
    # Reference: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=['Programming Language :: Python',
                 'Development Status :: 2 - Pre-Alpha',
                 'Natural Language :: English',
                 'Natural Language :: Japanese',
                 'Natural Language :: Indonesian',
                 'Environment :: Plugins',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: {}'.format(freebible.__license__),
                 'Operating System :: OS Independent',
                 'Topic :: Text Processing',
                 'Topic :: Software Development :: Libraries :: Python Modules']
)
