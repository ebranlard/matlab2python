import numpy as np
import unittest

from matlabparser.parsing_tools import *
# --------------------------------------------------------------------------------}
# ---  
# --------------------------------------------------------------------------------{
class TestParsingTools(unittest.TestCase):

    def assertEqual(self, first, second, msg=None):
        #print('\n>',first,'<',' >',second,'<')
        super(TestParsingTools, self).assertEqual(first, second, msg)

    def test_strings(self):
        self.assertEqual(string_contains_charset('g'  ,r'[a-z]'),True)
        self.assertEqual(string_contains_charset('09' ,r'[a-z]'),False)
        self.assertEqual(string_contains_charset('0g9',r'[a-z]'),True)
        self.assertEqual(previous_nonspace_pos ('01      8',8),1 )
        self.assertEqual(previous_nonspace_pos ('        8',8),-1)
        self.assertEqual(previous_nonspace_char('01      8',8),'1')
        self.assertEqual(previous_nonspace_char('        8',8),'')

    def test_quotes(self):
#         self.assertEqual(is_in_quotes("""0 '345' 7 """ ,4) ,True)
#         self.assertEqual(is_in_quotes("""01'345' 7 """ ,2) ,False)
        #self.assertEqual(is_in_quotes("""01'345' 7 """ ,6) ,False)
        self.assertEqual(replace_inquotes("""''""" ,'X') ,'XX')
        self.assertEqual(replace_inquotes("""0'23'5""" ,'X') ,'0XXXX5')
        self.assertEqual(replace_inquotes("""0'2"'5""" ,'X') ,'0XXXX5')
        self.assertEqual(replace_inquotes("""0"23"5""" ,'X') ,'0XXXX5')
        self.assertEqual(replace_inquotes("""0'2''5'7""" ,'X') ,'0XXXXXX7')
        self.assertEqual(replace_inquotes("""0'23""" ,'X') ,'0XXX')
        self.assertEqual(replace_inquotes("""0"23""" ,'X') ,'0XXX')
        self.assertEqual(extract_quotedstring("""''""") ,'')
        self.assertEqual(extract_quotedstring("""'a'""") ,'a')
        self.assertEqual(extract_quotedstring("""'a'b""") ,'a')
        self.assertEqual(extract_quotedstring("""'a""") ,'a')
        self.assertEqual(extract_quotedstring("""'a''a'""") ,'a\'\'a')
        self.assertEqual(extract_quotedstring("""'a"a'""") ,'a"a')
        self.assertEqual(extract_quotedstring('""') ,'')
        #print('>>>>>>>>>>>>>>')
        #print('>>>>>>>>>>>>>>')
        #print('>>>>>>>>>>>>>>')
        #print('>>>>>>>>>>>>>>')
        #self.assertEqual(separate_comment('s='i'),('  ','  '))
