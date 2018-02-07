#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Test script for heplpers module

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

from chirptext import TextReport

import freebible

# -------------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------------

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


def getLogger():
    return logging.getLogger(__name__)


# -------------------------------------------------------------------------------
# Tests
# -------------------------------------------------------------------------------

class TestHelpers(unittest.TestCase):

    def test_bibles(self):
        self.assertEqual(len(freebible.bibles.kougo), 66)
        self.assertEqual(len(freebible.bibles.web), 66)

    def test_quoting(self):
        output = TextReport()
        books = freebible.bibles.quote('John', output=output)
        self.assertTrue(books)
        for b in books:
            self.assertIsInstance(b, freebible.model.Book)
        chapters = freebible.bibles.quote('John', 1, output=output)
        self.assertTrue(chapters)
        for c in chapters:
            self.assertIsInstance(c, freebible.model.Chapter)
        verses = freebible.bibles.quote('John', 1, 1, output=output)
        self.assertTrue(verses)
        for v in verses:
            self.assertIsInstance(v, freebible.model.Verse)

    def test_printing(self):
        freebible.bibles.print('John')
        freebible.bibles.print('John', 1)
        freebible.bibles.print('John', 1, 1)


# -------------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
