# SMOP -- Simple Matlab/Octave to Python compiler
# Copyright 2011-2016 Victor Leikehman
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
from . import version


def parse_matlab_lines(buf, bckd='smop',no_resolve=False):
    s=''
    stmt_list = parse.parse(buf if buf[-1] == '\n' else buf + '\n')
    #print(stmt_list)
    if not no_resolve:
        G = resolve.resolve(stmt_list)
    if bckd=='smop':
        from . import backend
        s ="from libsmop import *\n"
        s+= backend.backend(stmt_list)
    elif bckd=='m2py':
        from . import backend_m2py
        s = backend_m2py.backend(stmt_list)
    else:
        s='\n'.join([s.__repr__() for s in stmt_list])
    return s

