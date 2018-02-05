#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Test script for bible parsers

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
import unittest
import logging

import freebible
from freebible.parsers.web import read_keys, read_verses, read_abbr, read_genres

# -------------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------------

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


def getLogger():
    return logging.getLogger(__name__)

# -------------------------------------------------------------------------------
# Tests
# -------------------------------------------------------------------------------


class TestKougoParser(unittest.TestCase):

    def test_parse_kougo(self):
        bible = freebible.read_kougo()
        cc = sum(len(b) for b in bible)
        cv = sum(b.verse_count() for b in bible)
        self.assertEqual(len(bible), 66)
        self.assertEqual(cc, 1189)
        self.assertEqual(cv, 31105)
        self.assertEqual(len(bible.keys()), 66)


class TestWEBParser(unittest.TestCase):

    def test_read_web_raw(self):
        books = read_keys(freebible.data.WEB_BOOKS)
        self.assertEqual(len(books), 66)
        self.assertEqual(books[0]['title'], 'Genesis')
        # test read genres
        genres = read_genres(freebible.data.WEB_GENRES)
        self.assertEqual(genres['1'], 'Law')
        # test read abbrs
        abbrs = read_abbr(freebible.data.WEB_ABBRS)
        self.assertEqual(abbrs.bid2name('1'), 'Gen')
        verses = read_verses(freebible.data.WEB_VERSES)
        self.assertEqual(len(verses), 31102)
        self.assertTrue(verses[0]['text'].startswith('In the beginning'))

    def test_read_web(self):
        bible = freebible.read_web()
        cc = sum(len(b) for b in bible)
        cv = sum(b.verse_count() for b in bible)
        self.assertEqual(len(bible), 66)
        self.assertEqual(cc, 1189)
        self.assertEqual(cv, 31102)
        self.assertEqual(len(bible.keys()), 66)


class TestCrossCheck(unittest.TestCase):

    def test_kougo_web_keys(self):
        kougo = freebible.read_kougo()
        web = freebible.read_web()
        abbrs = read_abbr(freebible.data.WEB_ABBRS)
        for b in kougo:
            std_abbr = abbrs.standardize(b.short_name)
            self.assertTrue(std_abbr)
            if not std_abbr:
                getLogger().warning("{} - {} not found".format(b.title_eng, b.short_name))
            self.assertIn(std_abbr, web)
        for b in web:
            self.assertIn(b.short_name, kougo)

    def test_verses(self):
        kougo = freebible.read_kougo()
        web = freebible.read_web()
        abbrs = read_abbr(freebible.data.WEB_ABBRS)
        for b in web:
            for c in b:
                for v in c:
                    try:
                        t = kougo[b.short_name][c.ID][v.ID]
                        assert t
                    except:
                        getLogger().warning("Missing verse in kougo {} {} {}".format(b.short_name, c.ID, v.ID))
        for b in kougo:
            for c in b:
                for v in c:
                    try:
                        t = web[abbrs.standardize(b.short_name)][c.ID][v.ID]
                        assert t
                    except:
                        getLogger().warning("Missing verse in WEB {} {} {}".format(b.short_name, c.ID, v.ID))


# -------------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
