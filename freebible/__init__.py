# -*- coding: utf-8 -*-

'''
Python Free Bible Toolkits
Latest version can be found at https://github.com/neocl/freebible

:copyright: (c) 2018, Le Tuan Anh <tuananh.ke@gmail.com>
:license: MIT, see LICENSE for more details.
'''

from .__version__ import __author__, __email__, __copyright__, __maintainer__
from .__version__ import __credits__, __license__, __description__, __url__
from .__version__ import __version_major__, __version_long__, __version__, __status__

from freebible.helpers import read_kougo, read_web, bibles
from freebible.model import Collection
__all__ = ['read_kougo', 'read_web', 'bibles', 'Collection',
           "__version__", "__author__", "__description__", "__copyright__"]
