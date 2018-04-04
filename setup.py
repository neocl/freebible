#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Setup script for freebible.

Latest version can be found at https://github.com/neocl/freebible

:copyright: (c) 2018 Le Tuan Anh <tuananh.ke@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import io
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


readme_file = 'README.rst' if os.path.isfile('README.rst') else 'README.md'
long_description = read(readme_file)
pkg_info = {}
exec(read('freebible/__version__.py'), pkg_info)

setup(
    name='freebible',
    version=pkg_info['__version__'],
    url=pkg_info['__url__'],
    project_urls={
        "Bug Tracker": "https://github.com/neocl/freebible/issues",
        "Source Code": "https://github.com/neocl/freebible/"
    },
    keywords="free holy bible nlp",
    license=pkg_info['__license__'],
    author=pkg_info['__author__'],
    tests_require=['chirptext >= 0.1a6'],
    install_requires=['chirptext >= 0.1a6'],
    author_email=pkg_info['__email__'],
    description=pkg_info['__description__'],
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
                 'Intended Audience :: Science/Research',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Religion',
                 'License :: OSI Approved :: {}'.format(pkg_info['__license__']),
                 'Operating System :: OS Independent',
                 'Topic :: Religion',
                 'Topic :: Text Processing',
                 'Topic :: Software Development :: Libraries :: Python Modules']
)
