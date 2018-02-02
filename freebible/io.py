# -*- coding: utf-8 -*-

'''
Common IO functions
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

import os
import logging
import codecs
import gzip
import csv


# -------------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------------

def getLogger():
    return logging.getLogger(__name__)


# -------------------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------------------

def is_file(path):
    return path and os.path.isfile(path)


def to_string(content, encoding='utf-8'):
    if isinstance(content, bytes):
        return content.decode(encoding)
    elif isinstance(content, str):
        return content
    else:
        return str(content)


def read_file(path, encoding='utf-8', *args, **kwargs):
    ''' Read text file content as a string. If the file name ends with .gz, read it as gzip file '''
    return process_file(path, processor=lambda x: to_string(x.read(), encoding),
                        encoding=encoding, *args, **kwargs)


def read_csv_file(path, fieldnames=None, encoding='utf-8', *args, **kwargs):
    ''' Read CSV from file as a list of lists of string.
        If the file name ends with .gz, read it as gzip file '''
    return process_file(path, processor=lambda f: [r for r in read_csv_iter(f, fieldnames=fieldnames)],
                        encoding=encoding, mode='rt', *args, **kwargs)


def read_csv_iter(input_stream, fieldnames=None):
    ''' Read CSV content as a table (list of lists) from an input stream '''
    if fieldnames:
        # read csv using dictreader
        reader = csv.DictReader(input_stream, fieldnames)
        for row in reader:
            yield row
    else:
        csvreader = csv.reader(input_stream)
        for row in csvreader:
            yield row


def process_file(path, processor, encoding='utf-8', mode='rt', *args, **kwargs):
    ''' Process a text file's content. If the file name ends with .gz, read it as gzip file '''
    if path.endswith('.gz'):
        with gzip.open(path, mode, encoding=encoding) as infile:
            return processor(infile)
    else:
        with codecs.open(path, mode=mode, encoding=encoding) as infile:
            return processor(infile)
