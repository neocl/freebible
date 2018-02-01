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
from freebible import read_kougo

# -------------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------------

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


# -------------------------------------------------------------------------------
# Tests
# -------------------------------------------------------------------------------


class TestParseKougo(unittest.TestCase):

    def test_parse_kougo(self):
        bible = read_kougo()
        cc = sum(len(b) for b in bible)
        cv = sum(b.verse_count() for b in bible)
        self.assertEqual(len(bible), 66)
        self.assertEqual(cc, 1189)
        self.assertEqual(cv, 31105)


# -------------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
