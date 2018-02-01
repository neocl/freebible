#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
A bible processing toolkit with free bible data for Python
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

from freebible.model import Collection, Book, Chapter, Verse


# -------------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------------

def getLogger():
    return logging.getLogger(__name__)


# -------------------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------------------

def parse_kougo(seisho_path):
    ''' Parse Kougo from raw text format '''
    if not seisho_path or not os.path.isfile(seisho_path):
        raise Exception("Seisho not found (provided path: {})".format(seisho_path))
    if seisho_path.endswith('.gz'):
        with gzip.open(seisho_path, 'rb') as infile:
            return parse_kougo_raw(infile.read().decode('utf-8'))
    else:
        with codecs.open(seisho_path, encoding='utf-8') as infile:
            return parse_kougo_raw(infile.read())


def parse_kougo_raw(kougo_content):
    lines = kougo_content.splitlines()
    getLogger().debug("Found {} verses.".format(len(lines)))
    assert lines[0].strip().endswith('=000 Bible begins')
    current_book = None
    books = []
    for idx, l in enumerate(lines[1:]):
        if l.startswith("="):
            if l == '=ALL':
                continue
            book = Book.from_string(l)
            if book is not None:
                books.append(book)
                current_book = book
        elif l == 'END ':
            if current_book is not None:
                current_book = None
            pass
        else:
            # a verse line
            v = Verse.from_string(l)
            if v is not None:
                if current_book is None:
                    getLogger().warning("Found an orphant verse: {}".format(v))
                elif v.chapID not in current_book:
                    current_book.add_chapter(Chapter(ID=v.chapID))
                # verify short name
                if not current_book.short_name:
                    current_book.short_name = v.book_key
                elif current_book.short_name != v.book_key:
                    getLogger().warning("Inconsistent book_key: {} vs {}".format(current_book.short_name, v.book_key))
                current_book[v.chapID].add_verse(v)
            else:
                print("ERROR:", idx, repr(l))
    # books to collection
    seisho = Collection()
    for b in books:
        seisho.add_book(b)
    return seisho
