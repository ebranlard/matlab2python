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
from . import version

def print_header(fp):
    #if options.no_header:
    #    return
    #print("# Running Python %s" % sys.version, file=fp)
    print("from libsmop import *", file=fp)

def parse_matlab_lines(buf, no_resolve=False):
    s=''
    stmt_list = parse.parse(buf if buf[-1] == '\n' else buf + '\n')
    #print(stmt_list)
    if not no_resolve:
        G = resolve.resolve(stmt_list)
    s = backend.backend(stmt_list)
    return s


# def main():
#     #if "M" in options.debug:
#     #    import pdb
#     #    pdb.set_trace()
#     #if not options.filelist:
#     #    options.parser.print_help()
#     #    return
#     if options.output == "-":
#         fp = sys.stdout
#     elif options.output:
#         fp = open(options.output, "w")
#     else:
#         fp = None
#     try:
#         buf = open(options.filename).read()
#         buf = buf.replace("\r\n", "\n")
#         stmt_list = parse.parse(buf if buf[-1] == '\n' else buf + '\n')
#         if not stmt_list:
#             continue
#         if not options.no_resolve:
#             G = resolve.resolve(stmt_list)
#         if not options.no_backend:
#             s = backend.backend(stmt_list)
#         if not options.output:
#             f = splitext(basename(options.filename))[0] + ".py"
#             with open(f, "w") as fp:
#                 print_header(fp)
#                 fp.write(s)
#         else:
#             fp.write(s)
#     except KeyboardInterrupt:
#         break
#     except:
#         traceback.print_exc(file=sys.stdout)
#         if options.strict:
#             break
#     finally:
#         pass
