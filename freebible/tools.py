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
import json

from chirptext import TextReport
from chirptext.cli import CLIApp, setup_logging

from freebible.model import Collection
from freebible.data import KOUGO_PATH
from freebible.parsers.kougo import parse_kougo

# -------------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------------

setup_logging('logging.json', 'logs')

MY_DIR = os.path.dirname(__file__)
DATA_FOLDER = os.path.join(MY_DIR, 'data')


# -------------------------------------------------------------------------------
# Application logic
# -------------------------------------------------------------------------------


def parse_bible(cli, args):
    ''' Parse raw bible data into freebible format '''
    rp = TextReport()
    if args.input:
        rp.print("Parsing kougo")
        kougo = parse_kougo(args.input)
        kougo.summarise()
    if args.output:
        rp.print("Exporting kougo to {}".format(args.output))
        with TextReport(args.output) as outfile:
            kougo.export(outfile, args.format)


def prompt():
    return input("Query (? or help): ")


def process(bible, query):
    try:
        if query in ('help', '?'):
            print("Available commands:")
            print("   + help: Display this help")
            print("   + books : List available books")
            print("   + quit or exit: Quit bible reader")
        elif query == 'books':
            print(' '.join(b.short_name for b in bible))
        elif query.lower() in ("quit", "exit"):
            print("Good bye. Have a nice day.")
            return False
        else:
            bn, cid, vid = query.split()
            print(bible[bn][cid][vid])
    except:
        print("Unknown command")
    return True


def read_bible(cli, args):
    if args.input and os.path.isfile(args.input):
        bible = Collection.read_json_file(args.input)
    else:
        # try to load from raw file
        bible = parse_kougo(KOUGO_PATH)
    bible.summarise()
    while True:
        query = prompt()
        if not process(bible, query):
            exit()


# -------------------------------------------------------------------------------
# Main method
# -------------------------------------------------------------------------------

def main():
    ''' freebible tools '''

    app = CLIApp(desc='Free Bible Toolkit for Python', logger=__name__)
    # add tasks
    task = app.add_task('parse', func=parse_bible)
    task.add_argument('-i', '--input', help='Input file', default=KOUGO_PATH)
    task.add_argument('-o', '--output', help='Output file')
    task.add_argument('-f', '--format', help='Output format (json, yaml, txt)', default='json', choices=['json', 'yaml', 'txt'])
    # bible read
    task = app.add_task('read', func=read_bible)
    task.add_argument('-i', '--input', help='Input file (JSON format)')
    # run app
    app.run()


if __name__ == "__main__":
    main()
