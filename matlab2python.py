#!/usr/bin/env python
from __future__ import absolute_import
import sys
import matlabparser
from matlabparser import parser

from smop.main import parse_matlab_lines

def main(inputfiles=[]):
    #Lines="""
    #function [j] = tamere(x)
    #x=3 % hello
    #% continuing
    #y.caca=2
    #j=4
    #"""
    #print(parse_matlab_lines(Lines))
#     pass
    matlabparser.parser.parse(inputfiles)



if __name__ == '__main__':
    main(sys.argv[1:])
