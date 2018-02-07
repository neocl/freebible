# -*- coding: utf-8 -*-

'''
Bible models
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
import re
import json
try:
    import yaml
except:
    logging.getLogger(__name__).warning("YAML module is not available. Exporting to YAML function will NOT work.")

from chirptext.anhxa import to_obj


# -------------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------------

DATA_FOLDER = os.path.abspath(os.path.expanduser('./data'))


def getLogger():
    return logging.getLogger(__name__)


# -------------------------------------------------------------------------------
# Data structures
# -------------------------------------------------------------------------------

class Collection(object):
    ''' Book collection '''
    def __init__(self, books=None):
        self.book_map = {}
        self.bookid_map = {}
        self.books = []
        if books is not None:
            for b in books:
                self.add_book(b)

    def __len__(self):
        return len(self.books)

    def __getitem__(self, key):
        return self.book_map[key]

    def __contains__(self, item):
        return item in self.book_map

    def __iter__(self):
        return iter(self.books)

    def quote(self, book_key, cid=None, vid=None):
        if book_key and cid and vid:
            return self[book_key][cid][vid]
        elif book_key and cid:
            return self[book_key][cid]
        elif book_key:
            return self[book_key]
        else:
            raise KeyError("Book key cannot be None")

    def add_book(self, book):
        self.book_map[book.short_name] = book
        self.bookid_map[book.ID] = book
        self.books.append(book)
        return book

    def keys(self):
        ''' Get a list of all available book keys (short names ) '''
        return [b.short_name for b in self]

    def summarise(self):
        cc = sum(len(b) for b in self)
        cv = sum(b.verse_count() for b in self.books)
        print("Available books: {}".format(len(self.books)))
        print("Available chaps: {}".format(cc))
        print("Available verses: {}".format(cv))

    @staticmethod
    def read_json(self, json_data):
        ''' Read bible as a Book Collection from json data '''
        books = [Book.from_json(b) for b in json_data]
        bible = Collection(books)
        return bible

    @staticmethod
    def read_json_file(self, json_filepath):
        ''' Read bible from a JSON file '''
        with open(json_filepath, 'r') as infile:
            return Collection.read_json(json.loads(infile.read()))

    def export(self, output, format='json'):
        json_books = [b.to_json() for b in self]
        if format == 'json':
            output.write(json.dumps(json_books, ensure_ascii=False, indent=2))
        elif format == 'yaml':
            try:
                yaml_str = yaml.safe_dump(json_books, default_flow_style=False, allow_unicode=True, encoding='utf-8')
                output.write(yaml_str)
            except:
                getLogger().exception("Error was raised while exporting to YAML format")
        elif format == 'txt':
            for b in self:
                for c in b:
                    for v in c:
                        output.write(v.text)
                        output.write('\n')
        else:
            raise Exception("Format {} is not supported".format(format))


class Book(object):

    TITLE_PTN = re.compile('=(?P<id>\d+) (?P<bookname>\w+) (?P<title>\w+(?: \(\w+\))?) - (?P<title_eng>[\w ]+)')

    def __init__(self, ID='', title='', filename='', title_eng='', short_name=''):
        """
        """
        self.ID = str(int(ID))
        self.filename = filename
        self.title = title
        self.title_eng = title_eng
        self.short_name = short_name
        self.__chapters = []
        self.__chapter_map = {}

    def add_chapter(self, chapter):
        if chapter.ID in self.__chapter_map:
            raise Exception("Chapter {} exists.".format(chapter.ID))
        else:
            self.__chapters.append(chapter)
            self.__chapter_map[chapter.ID] = chapter
            chapter.book = self
            return chapter

    def __getitem__(self, chapID):
        if chapID not in self.__chapter_map:
            return self.__chapter_map[str(chapID)]
        else:
            return self.__chapter_map[chapID]

    def __contains__(self, chapID):
        return chapID in self.__chapter_map

    def verse_count(self):
        return sum(len(c) for c in self)

    def __len__(self):
        return len(self.__chapters)

    def chapters(self):
        return list(self.__chapters)

    def __iter__(self):
        return iter(self.__chapters)

    @staticmethod
    def from_string(title_string):
        m = Book.TITLE_PTN.match(title_string)
        if m:
            return Book(ID=m.group('id'),
                        title=m.group('title'),
                        filename=m.group('bookname'),
                        title_eng=m.group('title_eng'))
        else:
            return None

    def __repr__(self):
        return "Book(ID={}, title={}, filename={}, title_eng={}, short_name={})".format(
            repr(self.ID), repr(self.title), repr(self.filename), repr(self.title_eng), repr(self.short_name))

    def __str__(self):
        return "[{}] {}".format(self.ID, self.title)

    def to_json(self):
        return {'ID': self.ID, 'filename': self.filename, 'title': self.title, 'title_eng': self.title_eng, 'short_name': self.short_name, 'chapters': [c.to_json() for c in self]}

    @staticmethod
    def from_json(json_dict):
        book = to_obj(Book, json_dict, 'ID', 'filename', 'title', 'title_eng', 'short_name')
        for chap in json_dict['chapters']:
            book.add_chapter(Chapter.from_json(chap))
        return book


class Chapter(object):

    def __init__(self, ID=None, title='', book=None):
        """
        """
        self.ID = ID
        self.title = title
        self.__verses = []
        self.__verse_map = {}
        self.__book = book

    @property
    def book(self):
        return self.__book

    @book.setter
    def book(self, value):
        self.__book = value

    def add_verse(self, verse):
        self.__verse_map[verse.ID] = verse
        self.__verses.append(verse)

    def __getitem__(self, key):
        if key not in self.__verse_map:
            return self.__verse_map[str(key)]
        else:
            return self.__verse_map[key]

    def __contains__(self, item):
        return item in self.__verse_map

    def verses(self):
        return list(self.__verses)

    def __len__(self):
        return len(self.__verses)

    def __iter__(self):
        return iter(self.__verses)

    def __repr__(self):
        return "Chapter(ID={})".format(repr(self.ID))

    def __str__(self):
        if self.__book:
            return "{} - chapter {}".format(self.book.title, self.ID)
        else:
            return "chapter {}".format(self.ID)

    def to_json(self):
        return {'ID': self.ID,
                'title': self.title,
                'verses': [v.to_json() for v in self]}

    @staticmethod
    def from_json(json_dict):
        chapter = to_obj(Chapter, json_dict, 'ID', 'title')
        # add verses
        for v in json_dict['verses']:
            chapter.add_verse(Verse.from_json(v))
        return chapter


class Verse(object):
    def __init__(self, ID='', text='', chapID='', book_key=''):
        """
        """
        self.ID = ID
        self.text = text
        self.chapID = chapID
        self.book_key = book_key

    def __str__(self):
        return "[{} {}:{}] {}".format(self.book_key, self.chapID, self.ID, self.text)

    def to_json(self):
        return {'ID': self.ID, 'text': self.text}

    def __repr__(self):
        return "{} {}:{} {}".format(self.book_key, self.chapID, self.ID, self.text)

    @staticmethod
    def from_json(json_dict):
        return to_obj(Verse, json_dict, 'ID', 'text', 'chapID', 'book_key')

    VERSE_PTN = re.compile('(?P<book_key>\w+) (?P<cid>\d+):(?P<vid>\d+) (?P<bookname>\w+) (?P<cid2>\d+):(?P<vid2>\d+) (?P<verse_text>.*)\s*')

    @staticmethod
    def from_string(verse_string):
        m = Verse.VERSE_PTN.match(verse_string)
        return Verse(ID=m.group('vid'), text=m.group('verse_text'), chapID=m.group('cid'), book_key=m.group('book_key'))


class BookMap(object):
    ''' Map book short names to standard book ID (WEB) '''
    def __init__(self, abbr_data):
        self.abbr_data = list(abbr_data)
        self.name_to_bid_map = {r['text']: r['bookID'] for r in self.abbr_data}
        self.bid_to_std_name_map = {r['bookID']: r['text'] for r in self.abbr_data if r['is_standard'] == '1'}
        # these abbrs are missing from WEB keys
        self.name_to_std_name_map = {'Deu': 'Deut',
                                     'Ruth': 'Rth',
                                     '1Sm': '1 Sam',
                                     '2Sm': '2 Sam',
                                     'Est': 'Esth',
                                     'Eccl': 'Eccles',
                                     'SSol': 'Song',
                                     'Jonah': 'Jnh',
                                     'Nahum': 'Nah',
                                     'Mat': 'Matt',
                                     'Mark': 'Mrk',
                                     'Luke': 'Luk',
                                     'Phi': 'Phil',
                                     'Phmn': 'Philem'}
        for row in abbr_data:
            self.name_to_std_name_map[row['text']] = self.bid2name(row['bookID'])

    def bid2name(self, bookID):
        ''' get standard short name for a bookID '''
        if bookID in self.bid_to_std_name_map:
            return self.bid_to_std_name_map[bookID]
        return None

    def name2bid(self, short_name):
        ''' Short name to bookID '''
        if short_name in self.name_to_bid_map:
            return self.name_to_bid_map[short_name]
        return None

    def standardize(self, short_name):
        if short_name in self.name_to_std_name_map:
            return self.name_to_std_name_map[short_name]
        else:
            return None
