"""
Difficulties
 A = [ 1 2 3  % comment
      4 5 5]
 A = { 1 2 3  % comment
      4 5 5}

 A = 

"""
import os
import unittest

from . import parsing_tools as PT

def strfind(s,c):
    return [pos for pos, char in enumerate(s) if char == c]

CHARSET_BEFORE_TRANSPOSE=r'[a-zA-Z0-9_\}\]\)\.\']'
CHARSET_BEFORE_TRANSPOSE_NONVAR=   r'[\}\]\)\.]'
CHARSET_VAR=r'[a-zA-Z0-9_]'


def find_strings(line):
    
    strings=[]
    i=0
    bUnfinished=False
    while i<len(line):
        c=line[i]
        if c=='\'':
            # Finding if it's a string start
            c_prev=line[i-1:i]
            if len(c_prev)==0:
                # for sure, it's a string start
                bStringStart=True
            elif PT.string_contains_charset(c_prev,CHARSET_BEFORE_TRANSPOSE):
                # for sure, it's a transpose
                bStringStart=False
            elif c_prev==' ':
                # that's tricky, let's see what's really before
                c_prev=PT.previous_nonspace_char(line,i)
                if len(c_prev)==0:
                    # for sure, it's a string start
                    bStringStart=True
                elif PT.string_contains_charset(c_prev,CHARSET_BEFORE_TRANSPOSE_NONVAR):
                    # for sure, it's a transpose
                    bStringStart=False
                elif PT.string_contains_charset(c_prev,CHARSET_VAR):
                    # That's the worse case, if you allow a space before a transpose: 
                    #   for instance [a ' ; b '] : is this a string concatenation? 
                    #       or concatenation of two transposed variables?
                    #print('>>> Potential problematic line, assuming string start:'+line)
                    bStringStart=True
                else:
                    # We could check for some syntax error here, but we can safely assume it's a string start
                    bStringStart=True
            else:
                bStringStart=True
            #
            if bStringStart:
                s = PT.extract_quotedstring(line[i:])
                if len(s)==len(line[i:])-1:
                    bUnfinished=True
                strings.append((i,s))
                i=i+1+len(s)
        i=i+1;



    return strings,bUnfinished

def replace_at_pos(s,pos,new):
    sout=s[0:pos]
    sout+=new
    sout+=s[pos+len(new):]
    return sout


def separate_comment(line):
    line_backup=line
    SI,bLastOK=find_strings(line)
    # Replacing strings with dummy 'X'
    for si in SI:
        line=replace_at_pos(line,si[0],'X'*(len(si[1])+2))
    pos=PT.find_pos(line,'%')
    if len(pos)==0:
        statement =line_backup
        comment =''
    else:
        comment   = line_backup[(pos[0]):]
        statement = line_backup[:(pos[0])]

    return statement, comment

def parse_function_def(stmt):
    stmt=stmt[8:].strip()
    name=''
    args_out=[]
    args_in=[]
    # Output arguments
    ieq=stmt.find('=')
    if ieq>0:
        sArgs_out=stmt[:ieq]
        sArgs_out=sArgs_out.replace('[','').replace(']','').replace(',','')
        args_out=[a.strip() for a in sArgs_out.split() if len(a)>0]
    # Declaration
    ieq = max(ieq+1,0)
    sDecl=stmt[ieq:].strip()
    # Function name
    io =sDecl.find('(')
    isc =sDecl.find(';')
    if io>0:
        name=sDecl[:io].strip()
    elif isc>0:
        name=sDecl[:isc].strip()
    else:
        name=sDecl.strip()
    # Arguments
    ic =sDecl.find(')')
    if io>0:
        args_in=[a.strip() for a in sDecl[io+1:ic].split(',') if len(a.strip())>0]
    return name, args_out, args_in

def parse_class_def(stmt):
    stmt=stmt[9:].strip().replace(';','');
    if len(stmt)==0:
        raise Exception('Wrong classdef definition')
    name=''
    children=[]
    im=stmt.find('<')
    if im>0:
        name=stmt[:im].strip()
        children=[a.strip() for a in stmt[im+1:].split(',') if len(a.strip())>0]
    else:
        name=stmt
    return name, children

def merge_lines(LC):
    LC_new=[]
    i=0
    while i<len(LC):
        lc=LC[i]
        stmt=lc[0].strip()
        if len(stmt)>0 and stmt[-1]=='\\':
            lc_next=LC[i+1]
            LC[i+1]=(stmt[:-1]+lc_next[0], lc[1]+lc_next[1])
        else:
            LC_new.append(lc)
        i+=1
    return LC_new



class TestParser(unittest.TestCase):

    def assertEqual(self, first, second, msg=None):
        #print('>',first,'<',' >',second,'<')
        super(TestParser, self).assertEqual(first, second, msg)

    def test_names(self):
        #self.assertEqual(extract_function_name('function y = f(a,b)'),'f'))
        self.assertEqual(parse_function_def('function y = f(a,b)'),('f',['y'],['a','b']))
        self.assertEqual(parse_function_def('function f;  '),('f',[],[]))
        self.assertEqual(parse_function_def('function f ; '),('f',[],[]))
        self.assertEqual(parse_function_def('function foo '),('foo',[],[]))
        self.assertEqual(parse_function_def('function foo() '),('foo',[],[]))
        self.assertEqual(parse_function_def('function foo ( ); '),('foo',[],[]))
        self.assertEqual(parse_function_def('function [a b] = f(c)'),('f',['a','b'],['c']))
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

class line():
    def __init__(self):
        self.statement=[]
        self.comment=[]

    def __init__(self,l):
        self.statement,self.comment = separate_comment(l)
# __all__  = ['parse']


class MatlabFile:
    def __init__(self,filename=None,lines=None):

        self.FileType=None #
        self.Properties=[] #
        self.Methods=[] #
        self.Header=[] #
        self.Corpus=[] #
        self.Name='' #
        self.ClassChildren='' #
        self.ArgsIn='' #
        self.ArgsOut='' #

        if filename is not None:
            with open(filename,'r') as f:
                self.raw_lines=f.readlines()
        elif lines is not None:
            self.raw_lines=lines
        else:
            raise Exception('Provide filename or lines')
        self.read()

    def read(self):
        # --- Separate lines and comments
        lines_comment=[]
        for l in self.raw_lines:
            lc=separate_comment(l.strip())
            #print(parse_matlab_lines(lc[0]+'\n'))
            lines_comment.append(lc)
        # --- Merging lines with explicit line continuation \
        lines_comment = merge_lines(lines_comment)
        #for lc in lines_comment:
        #    print(lc[0], lc[1])

        # --- detecting main file type and splitting into corpus and header
        self.Header=[]
        for lc in lines_comment:
            if self.FileType is None: 
                stmt=lc[0].strip().lower()
                if len(stmt)==0:
                    self.Header.append(lc)
                else:
                    if stmt.find('classdef')==0:
                        self.FileType='class'
                        self.Name = parse_class_def(lc[0])[0]
                        self.Corpus.append(lc)
                    elif stmt.find('function')==0:
                        self.FileType='function'
                        self.Name = parse_function_def(lc[0])[0]
                        self.Corpus.append(lc)
                    else:
                        self.FileType='script'
                        self.Corpus.append(lc)
            else:
                self.Corpus.append(lc)
        # --- For classes we detect properies and methods
        def remove_last_end(lc):
            if len(lc)>0:
                bEndFound=False
                i=len(lc)-1
                while not bEndFound and i>=0:
                    words = lc[i][0].strip().lower().split(';')
                    if 'end' in words:
                        bEndFound=True
                        lc[i]=(';'.join([w for w in words if w!='end']),lc[i][1])
                    i-=1
            return lc
        if self.FileType=='class':
            print('>>>> CLASS PARSING')
            bIsInProp=False
            bIsInMeth=False
            lProp=[]
            lMeth=[]
            self.Corpus = remove_last_end(self.Corpus) # removing end class
            for lc in self.Corpus[1:]:
                stmt=lc[0].strip().lower()
                if stmt.find('properties')==0:
                    bIsInProp=True
                    bIsInMeth=False
                    lProp=remove_last_end(lProp)
                elif stmt.find('methods')==0:
                    bIsInProp=False
                    bIsInMeth=True
                    lMeth=remove_last_end(lMeth)
                elif bIsInProp:
                    lProp.append(lc)
                elif bIsInMeth:
                    lMeth.append(lc)
                else:
                    pass
                    #self.Header.append(lc)
            lMeth = remove_last_end(lMeth)
            lProp = remove_last_end(lProp)
            self.Methods=[lc for lc in lMeth if ((len(lc[0].strip())>0) or ( len(lc[1].strip())>0))]
            for lc in self.Methods:
                print('m: ',lc[0])
            self.Properties=[lc for lc in lProp if ((len(lc[0].strip())>0) or ( len(lc[1].strip())>0))]
            for lc in self.Properties:
                print('p:',lc[0],lc[1])
            for lc in self.Header:
                print('h:',lc[0])

        def toString(self):
            pass




def parse(filename):
    from smop.main import parse_matlab_lines
    # Looping through files if a list provided
    if isinstance(filename,list):
        for f in filename:
            parse(f)
        return
    # Parsing
    print('Parsing: {}'.format(filename))
    if not os.path.exists(filename):
        raise Exception('FileNotFound:'+filename)

    MF=MatlabFile(filename=filename)
    #print(lines)



    
