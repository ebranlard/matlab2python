# SMOP -- Simple Matlab/Octave to Python compiler
# Copyright 2011-2016 Victor Leikehman

from __future__ import print_function

import py_compile
import tempfile
import fnmatch
import tarfile
import sys
import os
import traceback
from os.path import basename, splitext

from . import parse
from . import resolve
from . import backend
from . import backend_m2py
from . import version


def parse_matlab_lines(buf, backend='smop',no_resolve=False):
    s=''
    stmt_list = parse.parse(buf if buf[-1] == '\n' else buf + '\n')
    #print(stmt_list)
    if not no_resolve:
        G = resolve.resolve(stmt_list)
    if backend=='smop':
        s ="from libsmop import *\n"
        s+= backend.backend(stmt_list)
    elif backend=='m2py':
        s = backend_m2py.backend(stmt_list)
    else:
        s='\n'.join([s.__repr__() for s in stmt_list])
    return s

