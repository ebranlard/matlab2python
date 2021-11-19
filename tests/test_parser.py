import numpy as np
import unittest

from matlabparser.parser import *

# --------------------------------------------------------------------------------}
# ---  
# --------------------------------------------------------------------------------{
class TestParser(unittest.TestCase):

    def test_names(self):
        #self.assertEqual(extract_function_name('function y = f(a,b)'),'f'))
        self.assertEqual(parse_function_def('function y = f(a,b)'),('f',['y'],['a','b']))
        self.assertEqual(parse_function_def('function f;  '),('f',[],[]))
        self.assertEqual(parse_function_def('function f ; '),('f',[],[]))
        self.assertEqual(parse_function_def('function foo '),('foo',[],[]))
        self.assertEqual(parse_function_def('function foo() '),('foo',[],[]))
        self.assertEqual(parse_function_def('function foo ( ); '),('foo',[],[]))
        self.assertEqual(parse_function_def('function [a b] = f(c)'),('f',['a','b'],['c']))
        self.assertEqual(parse_function_def('function [a,b] = f(c)'),('f',['a','b'],['c']))
        self.assertEqual(parse_class_def('classdef y<h')    ,('y',['h']))
        self.assertEqual(parse_class_def('classdef y < h ;'),('y',['h']))
        self.assertEqual(parse_class_def('classdef y')      ,('y',[]))
        self.assertEqual(parse_class_def('classdef y;')     ,('y',[]))
        self.assertRaises(Exception,parse_class_def,'classdef')

    def test_comment(self):
        self.assertEqual(separate_comment(''),('',''))
        self.assertEqual(separate_comment('%%'),('','%%'))
        self.assertEqual(separate_comment(' %%'),(' ','%%'))
        self.assertEqual(separate_comment('%hi'),('','%hi'))
        self.assertEqual(separate_comment("""s='%' %com"""),("""s='%' """,'%com'))
        self.assertEqual(separate_comment("""A=B' %com"""),("""A=B' """,'%com'))
        self.assertEqual(separate_comment("""s='%';A=B' %com"""),("""s='%';A=B' """,'%com'))
        self.assertEqual(separate_comment("""s='%';A=B' %com '%com2"""),("""s='%';A=B' ""","""%com '%com2"""))

    def test_string(self):
        self.assertEqual(find_strings("""""")      ,([],False))
        self.assertEqual(find_strings("""AAAA""")  ,([],False))
        self.assertEqual(find_strings("""'""")     ,([(0,'')],True))
        self.assertEqual(find_strings("""''""")    ,([(0,'')],False))
        self.assertEqual(find_strings("""   'a'"""),([(3,'a')],False))
        self.assertEqual(find_strings("""x='a' """),([(2,'a')],False))
        self.assertEqual(find_strings("""x= 'a'"""),([(3,'a')],False))
        self.assertEqual(find_strings(""" x=A' """),([],False))
        self.assertEqual(find_strings(""" [0]' """),([],False))
        self.assertEqual(find_strings(""" x(:)' """),([],False))
        self.assertEqual(find_strings(""" {0}' """),([],False))
        self.assertEqual(find_strings("""  0.' """),([],False))
        self.assertEqual(find_strings("""  A'' """),([],False))
        self.assertEqual(find_strings(""" (A')' """),([],False))
        self.assertEqual(find_strings(""" [0]  ' """),([],False))
        self.assertEqual(find_strings(""" [a 'bbb'] """),([(4,'bbb')],False))
        self.assertEqual(find_strings("""f('it''s') """),([(2,"""it''s""")],False))
        self.assertEqual(find_strings("""x='a';y='b'"""),([(2,'a'),(8,'b')],False))

if __name__ == '__main__':
    unittest.main()
