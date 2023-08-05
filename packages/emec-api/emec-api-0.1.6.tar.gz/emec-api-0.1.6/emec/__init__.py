# -*- coding: utf-8 -*-

import emec
from emec import *

__author__ = 'Adilson Pavan'

VERSION = (0,1,6)

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    return version

__version__ = get_version()


