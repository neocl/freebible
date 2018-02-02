#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
World English Bible parser
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

import logging

from freebible.model import Collection, Book, Chapter, Verse, BookMap
from freebible.io import read_csv_file, is_file


# -------------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------------

def getLogger():
    return logging.getLogger(__name__)


# -------------------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------------------

def parse_web(path, book_path, abbr_path=None):
    ''' Parse WEB (World English Bible) from raw text format '''
    if not is_file(path) or not is_file(book_path):
        raise Exception("WEB data could not be found (provided path: {})".format(path))
    verses = read_verses(path)
    keys = read_keys(book_path)
    abbrs = read_abbr(abbr_path) if abbr_path else None
    return parse_web_raw(verses, keys, abbrs=abbrs)


def read_keys(path):
    return read_csv_file(path, fieldnames=('ID', 'title', 'col', 'genreID'))[1:]


def read_abbr(path):
    ''' return a BookMap object (for converting between bookID and short_name) '''
    abbr_data = read_csv_file(path, fieldnames=('ID', 'text', 'bookID', 'is_standard'))[1:]
    return BookMap(abbr_data)


def read_genres(path):
    rows = read_csv_file(path, fieldnames=('ID', 'genre'))[1:]
    return {row['ID']: row['genre'] for row in rows}


def read_verses(path):
    return read_csv_file(path, fieldnames=['ID', 'bookID', 'chapID', 'verseID', 'text'])[1:]


def parse_web_raw(verses, books, abbrs=None):
    bible = Collection()
    # add books
    for b in books:
        short_name = abbrs.bid2name(b['ID'])
        book_obj = Book(ID=b['ID'], title=b['title'], title_eng=b['title'], short_name=short_name)
        bible.add_book(book_obj)
    # add verses
    for idx, v in enumerate(verses):
        book = bible.bookid_map[v['bookID']]
        cid = v['chapID']
        if cid not in book:
            # create a new chapter
            chapter = Chapter(ID=cid)
            book.add_chapter(chapter)
        else:
            chapter = book[cid]
        # add verse to chapter
        verse_obj = Verse(ID=v['verseID'], text=v['text'], chapID=cid, book_key=book.short_name)
        chapter.add_verse(verse_obj)
    return bible
