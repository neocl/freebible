# -*- coding: utf-8 -*-

''' freebible test scripts
Latest version can be found at https://github.com/neocl/freebible

@author: Le Tuan Anh <tuananh.ke@gmail.com>
@license: MIT
'''

# This source code is a part of freebible library
# Copyright (c) 2018, Le Tuan Anh <tuananh.ke@gmail.com>
# LICENSE: The MIT License (MIT)
#
# Homepage: https://github.com/neocl/freebible

import os
from chirptext.cli import setup_logging

TEST_DIR = os.path.dirname(__file__)
TEST_DATA = os.path.join(TEST_DIR, 'data')

setup_logging(os.path.join(TEST_DIR, 'logging.json'), os.path.join(TEST_DIR, 'logs'))
